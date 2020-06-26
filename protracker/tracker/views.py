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


#Testing a graph view (trying to find a JS graph library that I like)
def graph(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)

    context = {
        'graph': graph,
        'goal': goal,
    }
    return render(request, 'tracker/graph.html', context)

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

        delta = goal.end_date - goal.created_date
        delta_range = delta.days + 1
        hours_per_day = goal.hours / delta_range

        # load up the arrays for chart.js
        for i in range(delta_range):
            day = goal.created_date + timedelta(days=i)
            labels_updated.append(day.date())
            timeline.append(hours_per_day*i)

        i = 0
        j = 0
        current_total = 0
        while i < len(timeline):
            day = goal.created_date + timedelta(days=i)
            if j < len(all_sessions):
                if day.date() in session_dates:
                    session_individual.append(session_hours[j])
                    current_total = current_total + session_hours[j]
                    sessions_total.append(current_total)
                    j +=1
            if day.date() not in session_dates:
                session_individual.append(0)
                sessions_total.append(current_total)
            i += 1

        data = {
            "labels": labels_updated,
            "timeline": timeline,
            "sessions_total": sessions_total,
            "sessions": session_individual
        }
        return Response(data)

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
    context = {
        'goal': goal,
    }
    return render(request, 'tracker/goal_detail.html', context)

@login_required
def milestone_detail(request, goal_id, milestone_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    milestone = get_object_or_404(Milestone, pk=milestone_id, goal=goal_id)
    context = {
        'goal': milestone.goal,
        'milestone': milestone,
    }
    return render(request, 'tracker/milestone_detail.html', context)

@login_required
def reward_detail(request, goal_id, reward_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    reward = get_object_or_404(Reward, pk=reward_id, goal=goal_id)
    context = {
        'goal': reward.goal,
        'milestone': reward.milestone,
        'reward': reward,
    }
    return render(request, 'tracker/reward_detail.html', context)

@login_required
def session_detail(request, goal_id, session_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    session = get_object_or_404(Session, pk=session_id, goal=goal_id)
    context = {
        'goal': session.goal,
        'milestone': session.milestone,
        'session': session,
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


### Record Edit Views
@login_required
def goal_edit(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    days_remaining = goal.end_date.replace(tzinfo=None) - datetime.datetime.now()
    if request.method == 'POST':
        form = GoalEdit(request.POST)
        if form.is_valid():
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
        form = GoalEdit()
    context = {
        'goal': goal,
        'form': form,
        'days_remaining': days_remaining.days,
    }
    return render(request, 'tracker/goal_edit.html', context)

@login_required
def milestone_edit(request, goal_id, milestone_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    days_remaining = milestone.end_date.replace(tzinfo=None) - datetime.datetime.now()
    if request.method == 'POST':
        form = MilestoneEdit(request.POST)
        if form.is_valid():
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
        form = GoalEdit()
    context = {
        'goal': goal,
        'milestone': milestone,
        'form': form,
        'days_remaining': days_remaining.days,
    }
    return render(request, 'tracker/milestone_edit.html', context)

@login_required
def reward_edit(request, goal_id, reward_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    reward = get_object_or_404(Reward, pk=reward_id)
    if request.method == 'POST':
        form = RewardEdit(request.POST)
        if form.is_valid():
            reward.milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            reward.description = request.POST['description']
            reward.save()
            return HttpResponseRedirect(reverse('tracker:reward detail', args=(goal.id, reward.milestone.id, reward.id,)))
    else:
        form = RewardEdit()
    context = {
        'goal': goal,
        'reward': reward,
        'form': form,
    }
    return render(request, 'tracker/reward_edit.html', context)

@login_required
def session_edit(request, goal_id, session_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.user != request.user:
        return render(request, 'tracker/forbidden.html', {})
    session = get_object_or_404(Session, pk=session_id)
    if request.method == 'POST':
        form = SessionEdit(request.POST)
        if form.is_valid():
            session.milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            session.description = request.POST['description']
            session.hour_count = request.POST['hour_count']
            session.difficulty = request.POST['difficulty']
            session.save()
            return HttpResponseRedirect(reverse('tracker:session detail', args=(goal.id, session.milestone.id, session.id,)))
    else:
        form = SessionEdit()
    context = {
        'goal': goal,
        'session': session,
        'form': form,
    }
    return render(request, 'tracker/session_edit.html', context)