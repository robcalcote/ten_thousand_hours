from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import *

import decimal

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


### Detail Views (See the details of each individual record)
class GoalDetailView(generic.DetailView):
    model = Goal

def milestone_detail(request, goal_id, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id, goal=goal_id)
    context = {
        'goal': milestone.goal,
        'milestone': milestone,
    }
    return render(request, 'tracker/milestone_detail.html', context)


### Record add pages (all will be created under their associated goal)
def goal_add(request):
    context = {}
    return render(request, 'tracker/goal_add.html', context)

def milestone_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    context = {
        'goal': goal,
    }
    return render(request, 'tracker/milestone_add.html', context)

def reward_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    context = {
        'goal': goal,
    }
    return render(request, 'tracker/reward_add.html', context)

def session_add(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    context = {
        'goal': goal,
    }
    return render(request, 'tracker/session_add.html', context)


### PROCESSING VIEWS
def process_totals(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    session_hour_count = decimal.Decimal(request.POST['session-hour-count'])
    if session_hour_count <= 0:
        # Redisplay the session add form.
        return render(request, 'tracker/session_add.html', {
            'goal': goal,
            'error_message': "You need to enter a value greater than 0",
        })
    else:
        goal.hours_remaining = goal.hours_remaining - session_hour_count
        goal.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tracker:updated', args=(goal.id,)))

def updated(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    return render(request, 'tracker/updated.html', {'goal': goal})




# TODO MONDAY!
# # Add These two views
# #     reward_view
# #     session_view
# # clean forms for:
# #     milestone
# #     session
# #     goal
# #     reward
# # Add necessary fields to DB
# # See notebook
def reward_view(request, goal_id, reward_id):
    return HttpResponse("You're looking at Reward %s." % reward_id)

def session_view(request, goal_id, session_id):
    return HttpResponse("You're looking at Session %s." % session_id)





def goal_edit(request, goal_id):
    return HttpResponse("You're looking at the edit page for Goal %s." %goal_id)

def milestone_edit(request, goal_id, milestone_id):
    return HttpResponse("You're looking at the edit page for Milestone %s." %milestone_id)

def reward_edit(request, goal_id, reward_id):
    return HttpResponse("You're looking at the edit page for Reward %s." % reward_id)

def session_edit(request, goal_id, session_id):
    return HttpResponse("You're looking at the edit page for Session %s." % session_id)



