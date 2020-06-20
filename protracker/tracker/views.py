from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import *

from .forms.forms import *

# generic python imports
import decimal
import datetime
from datetime import timedelta  

### MAIN DASHBOARD VIEW - HIGH OVERVIEW OF EVERYTHING
def dashboard(request):
    all_goals = Goal.objects.all()
    all_milestones = Milestone.objects.all()
    all_rewards = Reward.objects.all()
    all_sessions = Session.objects.all()
    context = {
        'all_goals': all_goals,
    }
    return render(request, 'tracker/dashboard.html', context)


### Detail Views
class GoalDetailView(generic.DetailView):
    model = Goal

def milestone_detail(request, goal_id, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id, goal=goal_id)
    context = {
        'goal': milestone.goal,
        'milestone': milestone,
    }
    return render(request, 'tracker/milestone_detail.html', context)

def reward_detail(request, goal_id, milestone_id, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id, goal=goal_id)
    context = {
        'goal': reward.goal,
        'milestone': reward.milestone,
        'reward': reward,
    }
    return render(request, 'tracker/reward_detail.html', context)

def session_detail(request, goal_id, milestone_id, session_id):
    session = get_object_or_404(Session, pk=session_id, goal=goal_id)
    context = {
        'goal': session.goal,
        'milestone': session.milestone,
        'session': session,
    }
    return render(request, 'tracker/session_detail.html', context)


### Record Add Views
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
            new_goal = Goal(description=desc, hours=hours, hours_remaining=hours_remaining,
                created_date=created_date, end_date=end_date, achieved_date=achieved_date)
            new_goal.save()
            return HttpResponseRedirect(reverse('tracker:dashboard'))
    else:
        form = GoalAdd()
    context = {
        'form': form,
    }
    return render(request, 'tracker/goal_add.html', context)

def milestone_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
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

def reward_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
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

def session_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SessionAdd(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # do stuff from form
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
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SessionAdd()
    context = {
        'goal': goal,
        'form': form,
    }
    return render(request, 'tracker/session_add.html', context)


### Record Edit Views
def goal_edit(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
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

def milestone_edit(request, goal_id, milestone_id):
    goal = get_object_or_404(Goal, pk=goal_id)
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

def reward_edit(request, goal_id, reward_id):
    goal = get_object_or_404(Goal, pk=goal_id)
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

def session_edit(request, goal_id, session_id):
    goal = get_object_or_404(Goal, pk=goal_id)
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