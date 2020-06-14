from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import *

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

### GOAL VIEWS
def goal_view(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    context = {
        'goal': goal,
    }
    return render(request, 'tracker/goal_view.html', context)





def goal_edit(request, goal_id):
    return HttpResponse("You're looking at the edit page for Goal %s." %goal_id)

def goal_add(request):
    return HttpResponse("Add a new goal here!")

### MILESTONE VIEWS
def milestone_view(request, goal_id, milestone_id):
    return HttpResponse("You're looking at Milestone %s." %milestone_id)

def milestone_edit(request, goal_id, milestone_id):
    return HttpResponse("You're looking at the edit page for Milestone %s." %milestone_id)

def milestone_add(request, goal_id):
    return HttpResponse("Add a new milestone here under Goal %s." % goal_id)
    
### REWARD VIEWS
def reward_view(request, goal_id, reward_id):
    return HttpResponse("You're looking at Reward %s." % reward_id)

def reward_edit(request, goal_id, reward_id):
    return HttpResponse("You're looking at the edit page for Reward %s." % reward_id)

def reward_add(request, goal_id):
    return HttpResponse("Add a new Reward here!")

### SESSION VIEWS
def session_edit(request, goal_id, session_id):
    return HttpResponse("You're looking at the edit page for Session %s." % session_id)

def session_add(request, goal_id):
    return HttpResponse("Add a new Session towards Goal %s." % goal_id)