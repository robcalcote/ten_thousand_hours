from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import *

from .forms.forms import SessionAdd

# generic python imports
import decimal
import datetime

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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SessionAdd(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # do stuff from form
            session_hour_count = decimal.Decimal(request.POST['hour_count'])
            milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
            date = datetime.datetime.now()
            difficulty = request.POST['difficulty']

            new_session = Session(goal=goal, milestone=milestone, date=date, 
                hour_count=session_hour_count, difficulty=difficulty)
            new_session.save()

            goal.hours_remaining = goal.hours_remaining - session_hour_count
            goal.save()

            milestone.hours_remaining = milestone.hours_remaining - session_hour_count
            milestone.save()

            return HttpResponseRedirect(reverse('tracker:updated', args=(goal.id,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SessionAdd()
    context = {
        'goal': goal,
        'form': form,
    }
    return render(request, 'tracker/session_add.html', context)


def updated(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    context = {
        'goal': goal,
    }
    return render(request, 'tracker/updated.html', context)




# TODO MONDAY!
#x# Add These two views
#x#     reward_view
#x#     session_view
#x#     links from goal -> other record detail view
# # clean forms for:
# #     milestone
# #     goal
# #     reward
#x#     session
# # Add necessary fields to DB
# # See notebook






def goal_edit(request, goal_id):
    return HttpResponse("You're looking at the edit page for Goal %s." %goal_id)

def milestone_edit(request, goal_id, milestone_id):
    return HttpResponse("You're looking at the edit page for Milestone %s." %milestone_id)

def reward_edit(request, goal_id, reward_id):
    return HttpResponse("You're looking at the edit page for Reward %s." % reward_id)

def session_edit(request, goal_id, session_id):
    return HttpResponse("You're looking at the edit page for Session %s." % session_id)



