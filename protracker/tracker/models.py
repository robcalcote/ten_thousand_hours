from django.db import models

### TODO -
### add the options for the fields in models
### Goal
#    Remove Admin Requirement for achieved_date
#    DateTime -> Date.auto_now

### Milestone
#    Add Description Field
#        update __str__ method

### Reward
#    Remove Admin Requirement for achieved_date
#    DateTime -> Date.auto_now
#    add field for picture of the reward

### Session
#    Remove Admin Requirement for achieved_date
#    DateTime -> Date.auto_now




# Create your models here.
class Goal(models.Model):
    description = models.TextField('description of goal')
    hours = models.SmallIntegerField('amount of hours in goal')
    hours_remaining = models.DecimalField('hours remaining', max_digits=10, decimal_places=2)
    created_date = models.DateTimeField('date created')
    end_date = models.DateTimeField('end date', null=True)
    achieved_date = models.DateTimeField('date achieved', null=True)
    def __str__(self):
        return self.description

class Milestone(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    hours = models.SmallIntegerField('amount of hours in milestone')
    hours_remaining = models.DecimalField('hours remaining', max_digits=10, decimal_places=2)
    created_date = models.DateTimeField('date created')
    end_date = models.DateTimeField('end date', null=True)
    achieved_date = models.DateTimeField('date achieved', null=True)

class Reward(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    description = models.TextField('description of reward')
    created_date = models.DateTimeField('date created')
    rewarded_date = models.DateTimeField('date rewarded', null=True)
    def __str__(self):
        return self.description

class Session(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT)
    milestone = models.ForeignKey(Milestone, on_delete=models.PROTECT)
    date = models.DateTimeField('date of session')
    hour_count = models.DecimalField('amount of hours', max_digits=4, decimal_places=2)
    DIFFICULTY_LEVEL = (
        # Moderate Difficulty is the default
        ('1', 'Very Easy'),
        ('2', 'Easy'),
        ('3', 'Moderate'),
        ('4', 'Hard'),
        ('5', 'Very Hard'),
    )
    difficulty = models.CharField('difficulty level', db_index=True, choices=DIFFICULTY_LEVEL, default=DIFFICULTY_LEVEL[2][0], max_length=1)