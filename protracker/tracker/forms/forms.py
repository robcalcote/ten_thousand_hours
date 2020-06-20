from django import forms

# RECORD ADD FORMS
class GoalAdd(forms.Form):
    description = forms.CharField(label='description of goal', widget=forms.Textarea)
    hours = forms.IntegerField(label='amount of hours in goal', min_value=0, max_value=99999)
    end_date = forms.IntegerField(label='in how many days do you want to achieve your goal?', min_value=0, max_value=9999)

class MilestoneAdd(forms.Form):
    description = forms.CharField(label='description of milestone', widget=forms.Textarea)
    hours = forms.IntegerField(label='amount of hours in milestone', min_value=0, max_value=9999)
    end_date = forms.IntegerField(label='in how many days do you want to achieve your milestone?', min_value=0, max_value=9999)

class RewardAdd(forms.Form):
    description = forms.CharField(label='description of reward', widget=forms.Textarea)
    # photo = forms.ImageField(label='picture of your reward')

class SessionAdd(forms.Form):
    description = forms.CharField(label='description of session', widget=forms.Textarea)
    hour_count = forms.DecimalField(label='number of hours')
    difficulty = forms.IntegerField(label= 'difficulty level', min_value=1, max_value=5)


# RECORD EDIT FORMS
class GoalEdit(forms.Form):
    description = forms.CharField(label='description of goal', widget=forms.Textarea)
    hours = forms.IntegerField(label='amount of hours in goal', min_value=0, max_value=99999)
    end_date = forms.IntegerField(label='in how many days do you want to achieve your goal?', min_value=0, max_value=9999)

class MilestoneEdit(forms.Form):
    description = forms.CharField(label='description of milestone', widget=forms.Textarea)
    hours = forms.IntegerField(label='amount of hours in milestone', min_value=0, max_value=99999)
    end_date = forms.IntegerField(label='in how many days do you want to achieve your milestone?', min_value=0, max_value=9999)

class RewardEdit(forms.Form):
    description = forms.CharField(label='description of reward', widget=forms.Textarea)
    # photo = forms.ImageField(label='picture of your reward')

class SessionEdit(forms.Form):
    description = forms.CharField(label='description of session', widget=forms.Textarea)
    hour_count = forms.DecimalField(label='number of hours')
    difficulty = forms.IntegerField(label= 'difficulty level', min_value=1, max_value=5)