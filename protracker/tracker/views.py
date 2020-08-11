from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

# project speicifc imports
from .models import *
from .forms.forms import *

# generic python imports
import decimal
from decimal import *
import datetime
from datetime import date, timedelta  

# Django REST framework imports
from rest_framework.views import APIView
from rest_framework.response import Response

### Auth Views
def user_login(request):
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('tracker:dashboard'))
    else:
        form = LoginUser()
    context = {
        'form': form
    }
    return render(request, 'tracker/user_login.html', context)

def user_register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('tracker:user login'))
    else:
        form = RegisterUser()
    context = {
        'form': form
    }
    return render(request, 'tracker/user_register.html', context)  
    
def user_logout(request):
    logout(request)
    form = LoginUser()
    context = {
        'form': form,
    }
    return render(request, 'tracker/user_login.html', context)

### MAIN DASHBOARD VIEW - HIGH OVERVIEW OF EVERYTHING
@login_required
def dashboard(request):
    user = request.user.id
    all_goals = Goal.objects.filter(user=user)
    all_milestones = Milestone.objects.filter(goal__user=user)
    all_rewards = Reward.objects.filter(goal__user=user)
    all_sessions = Session.objects.filter(goal__user=user)
    context = {
        'all_goals': all_goals,
        'all_milestones': all_milestones,
        'all_rewards': all_rewards,
        'all_sessions': all_sessions,
    }
    return render(request, 'tracker/dashboard.html', context)

### Detail Views
@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    goal = get_object_or_404(Goal, pk=goal_id)
    sessions = goal.session_set.order_by('-date')
    days_remaining = goal.end_date.replace(tzinfo=None) - datetime.datetime.now()


    ## FORMS - goal_edit, milestone_add, reward_add, session_add
    # goal_edit
    if "goal_edit_submit" in request.POST:
        form_goal_edit = GoalEdit(request.POST)
        if form_goal_edit.is_valid():
            ## This needs some major editing
            # goal.end_date is acting strangely - sometimes removing a day
            goal.description = request.POST['description']
            goal.hours = request.POST['hours']
            hours_remaining = decimal.Decimal(request.POST['hours'])
            sessions = Session.objects.filter(goal=goal)
            for session in sessions:
                hours_remaining = hours_remaining - session.hour_count
            goal.hours_remaining = hours_remaining
            goal.end_date = datetime.datetime.now() + timedelta(days=int(request.POST['end_date'])+1)
            goal.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form_goal_edit = GoalEdit()
    # milestone_add
    if "milestone_add_submit" in request.POST:
        form_milestone_add = MilestoneAdd(request.POST)
        if form_milestone_add.is_valid():
            desc = request.POST['description']
            hours = request.POST['hours']
            hours_remaining = request.POST['hours']
            created_date = datetime.datetime.now()
            end_date = created_date + timedelta(days=int(request.POST['end_date']))
            achieved_date = None
            new_milestone = Milestone(goal=goal, description=desc, hours=hours, hours_remaining=hours_remaining,
                created_date=created_date, end_date=end_date, achieved_date=achieved_date)
            new_milestone.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form_milestone_add = MilestoneAdd()
    # reward_add
    if "reward_add_submit" in request.POST:
        form_reward_add = RewardAdd(request.POST, request.FILES)
        if form_reward_add.is_valid():
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            desc = request.POST['description']
            created_date = datetime.datetime.now()
            rewarded = None
            # handle_uploaded_file(request.FILES['photo'], milestone.id)
            new_reward = Reward(goal=goal, milestone=milestone, description=desc, created_date=created_date, 
                rewarded_date=None)
            new_reward.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form_reward_add = RewardAdd()
    # session_add
    if "session_add_submit" in request.POST:
        form_session_add = SessionAdd(request.POST)
        if form_session_add.is_valid():
            desc = request.POST['description']
            session_hour_count = decimal.Decimal(request.POST['hour_count'])
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            date = datetime.datetime.now()
            difficulty = request.POST['difficulty']
            new_session = Session(goal=goal, milestone=milestone, description=desc, date=date, 
                hour_count=session_hour_count, difficulty=difficulty)
            new_session.save()
            goal.hours_remaining = goal.hours_remaining - session_hour_count
            goal.save()
            milestone.hours_remaining = milestone.hours_remaining - session_hour_count
            milestone.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form_session_add = SessionAdd()

    context = {
        'goal': goal,
        'sessions': sessions,
        'days_remaining': days_remaining.days,
        'form_goal_edit': form_goal_edit,
        'form_milestone_add': form_milestone_add,
        'form_reward_add': form_reward_add,
        'form_session_add': form_session_add,

    }
    return render(request, 'tracker/goal_detail.html', context)

### Chart.js view within the goal_detail view
class GraphData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, goal_id, format=JsonResponse):
        goal = get_object_or_404(Goal, pk=goal_id)

        all_sessions = Session.objects.filter(goal=goal)
        session_hours = [session.hour_count for session in goal.session_set.all()]
        session_dates = [session.date.date() for session in goal.session_set.all()]

        #context lists
        labels_updated = []
        timeline = []
        sessions_total = []
        session_individual = []

        #these variables are used for timeline calculations
        delta = goal.end_date - goal.created_date
        delta_range = delta.days + 1
        hours_per_day = goal.hours / delta_range

        #working on displaying only the preceding and following week...
        todays_date = datetime.date.today()
        week_ago = todays_date - datetime.timedelta(days=7)
        week_forward = todays_date + datetime.timedelta(days=7)
        delta_from_start = week_ago - goal.created_date.date()

        two_week_delta = week_forward - week_ago
        for date in range(two_week_delta.days + 1):
            display_day = week_ago + timedelta(days=date)
            # this is the date label - keep this as is
            labels_updated.append(display_day)
            # this is correctly showing where you SHOULD be at, to be on target, starting from a week ago,
            # to a week in the future
            if (((hours_per_day*date)+(hours_per_day*delta_from_start.days)) <= goal.hours):
                timeline.append((hours_per_day*date)+(hours_per_day*delta_from_start.days))
            else:
                timeline.append(goal.hours)

        # this variable is used to be a holder for all the previous hours added
        total_previous_hours = 0.0
        # this variable holds all the sessions that math must be done on
        sessions_to_calculate = []
        sessions_to_calculate_hours = []
        for session in goal.session_set.all().order_by('date'):
            if session.date.date() < week_ago:
                total_previous_hours += float(session.hour_count)
            if session.date.date() in labels_updated:
                sessions_to_calculate.append(session.date.date())
                sessions_to_calculate_hours.append(session.hour_count)

        # tracks current total
        i = 0
        # tracks individual sessions
        j = 0
        current_total = Decimal(total_previous_hours)
        while i < 15:
            day = week_ago + timedelta(days=i)
            if j < len(sessions_to_calculate):
                if day in sessions_to_calculate:
                    session_individual.append(sessions_to_calculate_hours[j])
                    current_total = current_total + sessions_to_calculate_hours[j]
                    sessions_total.append(current_total)
                    j += 1
            if day not in sessions_to_calculate:
                session_individual.append(None)
                sessions_total.append(current_total)
            i +=1

        data = {
            "labels": labels_updated,
            "timeline": timeline,
            "sessions_total": sessions_total,
            "sessions": session_individual
        }
        return Response(data)

@login_required
def milestone_detail(request, goal_id, milestone_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    milestone = get_object_or_404(Milestone, pk=milestone_id, goal=goal_id)
    sessions = milestone.session_set.order_by('-date')
    days_remaining = milestone.end_date.replace(tzinfo=None) - datetime.datetime.now()
    
    ## FORMS - milestone_edit, reward_add, session_add
    # milestone_edit
    if "milestone_edit_submit" in request.POST:
        form_milestone_edit = MilestoneEdit(request.POST)
        if form_milestone_edit.is_valid():
            ## This needs some major editing
            # milestone.end_date is acting strangely - sometimes removing a day
            milestone.description = request.POST['description']
            milestone.hours = request.POST['hours']
            hours_remaining = decimal.Decimal(request.POST['hours'])
            sessions = Session.objects.filter(milestone=milestone)
            for session in sessions:
                hours_remaining = hours_remaining - session.hour_count
            milestone.hours_remaining = hours_remaining
            milestone.end_date = datetime.datetime.now() + timedelta(days=int(request.POST['end_date'])+1)
            milestone.save()
            return HttpResponseRedirect(reverse('tracker:milestone detail', args=(goal.id, milestone.id,)))
    else:
        form_milestone_edit = GoalEdit()
    # reward_add
    if "reward_add_submit" in request.POST:
        form_reward_add = RewardAdd(request.POST, request.FILES)
        if form_reward_add.is_valid():
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            desc = request.POST['description']
            created_date = datetime.datetime.now()
            rewarded = None
            # handle_uploaded_file(request.FILES['photo'], milestone.id)
            new_reward = Reward(goal=goal, milestone=milestone, description=desc, created_date=created_date, 
                rewarded_date=None)
            new_reward.save()
            return HttpResponseRedirect(reverse('tracker:milestone detail', args=(goal.id, milestone.id,)))
    else:
        form_reward_add = RewardAdd()
    # session_add
    if "session_add_submit" in request.POST:
        form_session_add = SessionAdd(request.POST)
        if form_session_add.is_valid():
            desc = request.POST['description']
            session_hour_count = decimal.Decimal(request.POST['hour_count'])
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            date = datetime.datetime.now()
            difficulty = request.POST['difficulty']
            new_session = Session(goal=goal, milestone=milestone, description=desc, date=date, 
                hour_count=session_hour_count, difficulty=difficulty)
            new_session.save()
            goal.hours_remaining = goal.hours_remaining - session_hour_count
            goal.save()
            milestone.hours_remaining = milestone.hours_remaining - session_hour_count
            milestone.save()
            return HttpResponseRedirect(reverse('tracker:milestone detail', args=(goal.id, milestone.id,)))
    else:
        form_session_add = SessionAdd()
    
    context = {
        'goal': milestone.goal,
        'milestone': milestone,
        'sessions': sessions,
        'days_remaining': days_remaining.days,
        'form_milestone_edit': form_milestone_edit,
        'form_reward_add': form_reward_add,
        'form_session_add': form_session_add,
    }
    return render(request, 'tracker/milestone_detail.html', context)

@login_required
def reward_detail(request, goal_id, reward_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    reward = get_object_or_404(Reward, pk=reward_id, goal=goal_id)
    rewarded = reward.rewarded_date.date() < datetime.date.today()
    percent_complete = (reward.milestone.hours - reward.milestone.hours_remaining) / reward.milestone.hours
    sessions = reward.milestone.session_set.all().order_by('date')

    ## FORMS - reward_edit, session_add
    # reward_edit
    if "reward_edit_submit" in request.POST:
        form_reward_edit = RewardEdit(request.POST)
        if form_reward_edit.is_valid():
            reward.milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            reward.description = request.POST['description']
            reward.save()
            return HttpResponseRedirect(reverse('tracker:reward detail', args=(goal.id, reward.id,)))
    else:
        form_reward_edit = RewardEdit()
    # session_add
    if "session_add_submit" in request.POST:
        form_session_add = SessionAdd(request.POST)
        if form_session_add.is_valid():
            desc = request.POST['description']
            session_hour_count = decimal.Decimal(request.POST['hour_count'])
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            date = datetime.datetime.now()
            difficulty = request.POST['difficulty']
            new_session = Session(goal=goal, milestone=milestone, description=desc, date=date, 
                hour_count=session_hour_count, difficulty=difficulty)
            new_session.save()
            goal.hours_remaining = goal.hours_remaining - session_hour_count
            goal.save()
            milestone.hours_remaining = milestone.hours_remaining - session_hour_count
            milestone.save()
            return HttpResponseRedirect(reverse('tracker:reward detail', args=(goal.id, reward.id,)))
    else:
        form_session_add = SessionAdd()
    context = {
        'goal': reward.goal,
        'milestone': reward.milestone,
        'reward': reward,
        'rewarded': rewarded,
        'percent_complete': "{:.2%}".format(percent_complete),
        'sessions': sessions,
        'form_reward_edit': form_reward_edit,
        'form_session_add': form_session_add,
    }
    return render(request, 'tracker/reward_detail.html', context)

@login_required
def session_detail(request, goal_id, session_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    session = get_object_or_404(Session, pk=session_id, goal=goal_id)
    
    ## FORMS - session_edit
    # session_edit
    if "session_edit_submit" in request.POST:
        form_session_edit = SessionEdit(request.POST)
        if form_session_edit.is_valid():
            session.milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            session.description = request.POST['description']
            session.hour_count = request.POST['hour_count']
            session.difficulty = request.POST['difficulty']
            session.save()
            return HttpResponseRedirect(reverse('tracker:session detail', args=(goal.id, session.id,)))
    else:
        form_session_edit = SessionEdit()
    context = {
        'goal': session.goal,
        'milestone': session.milestone,
        'session': session,
        'form_session_edit': form_session_edit,
    }
    return render(request, 'tracker/session_detail.html', context)



### Record Add Views
@login_required
def goal_add(request):
    if request.method == 'POST':
        form = GoalAdd(request.POST)
        if form.is_valid():
            desc = request.POST['description']
            hours = request.POST['hours']
            hours_remaining = request.POST['hours']
            created_date = datetime.datetime.now()
            end_date = created_date + timedelta(days=int(request.POST['end_date']))
            achieved_date = None
            new_goal = Goal(user=request.user, description=desc, hours=hours, hours_remaining=hours_remaining,
                created_date=created_date, end_date=end_date, achieved_date=achieved_date)
            new_goal.save()
            return HttpResponseRedirect(reverse('tracker:dashboard'))
    else:
        form = GoalAdd()
    context = {
        'form': form,
    }
    return render(request, 'tracker/goal_add.html', context)

@login_required
def milestone_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    if request.method == 'POST':
        form = MilestoneAdd(request.POST)
        if form.is_valid():
            desc = request.POST['description']
            hours = request.POST['hours']
            hours_remaining = request.POST['hours']
            created_date = datetime.datetime.now()
            end_date = created_date + timedelta(days=int(request.POST['end_date']))
            achieved_date = None
            new_milestone = Milestone(goal=goal, description=desc, hours=hours, hours_remaining=hours_remaining,
                created_date=created_date, end_date=end_date, achieved_date=achieved_date)
            new_milestone.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form = MilestoneAdd()
    context = {
        'goal': goal,
        'form': form,
    }
    return render(request, 'tracker/milestone_add.html', context)


# def handle_uploaded_file(photo, milestone):
#     with open(str(milestone), 'wb+') as destination:
#         for chunk in photo.chunks():
#             destination.write(chunk)

@login_required
def reward_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    if request.method == 'POST':
        form = RewardAdd(request.POST, request.FILES)
        if form.is_valid():
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            desc = request.POST['description']
            created_date = datetime.datetime.now()
            rewarded = None
            # handle_uploaded_file(request.FILES['photo'], milestone.id)
            new_reward = Reward(goal=goal, milestone=milestone, description=desc, created_date=created_date, 
                rewarded_date=None)
            new_reward.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form = RewardAdd()
    context = {
        'goal': goal,
        'form': form,
    }
    return render(request, 'tracker/reward_add.html', context)

@login_required
def session_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    if request.method == 'POST':
        form = SessionAdd(request.POST)
        if form.is_valid():
            desc = request.POST['description']
            session_hour_count = decimal.Decimal(request.POST['hour_count'])
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            date = datetime.datetime.now()
            difficulty = request.POST['difficulty']
            new_session = Session(goal=goal, milestone=milestone, description=desc, date=date, 
                hour_count=session_hour_count, difficulty=difficulty)
            new_session.save()
            goal.hours_remaining = goal.hours_remaining - session_hour_count
            goal.save()
            milestone.hours_remaining = milestone.hours_remaining - session_hour_count
            milestone.save()
            return HttpResponseRedirect(reverse('tracker:goal detail', args=(goal.id,)))
    else:
        form = SessionAdd()
    context = {
        'goal': goal,
        'form': form,
    }
    return render(request, 'tracker/session_add.html', context)