from django.test import TestCase
import decimal

from .models import *

# Create your tests here.
class GoalModelTests(TestCase):
    
    def goal_cannot_have_less_than_0_hours_remaining(self):
        """
        Tests that a goal.hours_remaining cannot be less than 0
        """
        negative_hours_remaining = Goal(hours_remaining=-1)
        self.assertIs(negative_hours_remaining, False)