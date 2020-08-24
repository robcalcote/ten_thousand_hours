from tracker.forms.forms import *
from django.shortcuts import get_object_or_404
from .models import *


import decimal
from decimal import *
import datetime
from datetime import timedelta

def goal_add_form(request):
    form_goal_add = GoalAdd(request.POST)
    if form_goal_add.is_valid():
        user = request.user
        desc = request.POST['description']
        hours = request.POST['hours']
        hours_remaining = request.POST['hours']
        created_date = datetime.datetime.now()
        end_date = created_date + timedelta(days=int(request.POST['end_date']))
        achieved_date = None
        new_goal = Goal(user=user, description=desc, hours=hours, hours_remaining=hours_remaining,
            created_date=created_date, end_date=end_date, achieved_date=achieved_date)
        new_goal.save()

def milestone_add_form(request, goal):
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

def reward_add_form(request, goal):
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

def session_add_form(request, goal):
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
        goal.percent_remaining = 100 * (goal.hours_remaining / Decimal(goal.hours))
        goal.percent_complete = 100 - goal.percent_remaining
        goal.save()
        milestone.hours_remaining = milestone.hours_remaining - session_hour_count
        milestone.save()

def goal_edit_form(request, goal):
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

def milestone_edit_form(request, goal):
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

def reward_edit_form(request, goal):
    form_reward_edit = RewardEdit(request.POST)
    if form_reward_edit.is_valid():
        reward.milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
        reward.description = request.POST['description']
        reward.save()

def session_edit_form(request, goal):
    form_session_edit = SessionEdit(request.POST)
    if form_session_edit.is_valid():
        session.milestone = get_object_or_404(Milestone, pk=request.POST['milestone'])
        session.description = request.POST['description']
        session.hour_count = request.POST['hour_count']
        session.difficulty = request.POST['difficulty']
        session.save()