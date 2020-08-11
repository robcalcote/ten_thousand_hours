from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)

# importing Django's built-in and saving it (in case we want to do future customizations)
User = get_user_model()

#ACCOUNTS FORMS
class LoginUser(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Password Incorrect')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return super(LoginUser, self).clean(*args, **kwargs)

class RegisterUser(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already being used')
        return super(RegisterUser, self).clean(*args, **kwargs)


# RECORD ADD FORMS
class GoalAdd(forms.Form):
    description = forms.CharField(label='description of goal', widget=forms.Textarea(attrs={'placeholder' : 'Goal Description'}))
    hours = forms.IntegerField(label='amount of hours in goal', min_value=0, max_value=99999, widget=forms.NumberInput(attrs={'placeholder': 'Number of Hours'}))
    end_date = forms.IntegerField(label='in how many days do you want to achieve your goal?', min_value=0, max_value=9999, widget=forms.NumberInput(attrs={'placeholder': 'Number of Days'}))

class MilestoneAdd(forms.Form):
    description = forms.CharField(label='description of milestone', widget=forms.Textarea(attrs={'placeholder' : 'Milestone Description'}))
    hours = forms.IntegerField(label='amount of hours in milestone', min_value=0, max_value=9999, widget=forms.NumberInput(attrs={'placeholder' : 'Number of Hours'}))
    end_date = forms.IntegerField(label='in how many days do you want to achieve your milestone?', min_value=0, max_value=9999, widget=forms.NumberInput(attrs={'placeholder': 'Number of Days'}))

class RewardAdd(forms.Form):
    description = forms.CharField(label='description of reward', widget=forms.Textarea(attrs={'placeholder' : 'Reward Description'}))
    # photo = forms.ImageField(label='picture of your reward')

class SessionAdd(forms.Form):
    description = forms.CharField(label='description of session', widget=forms.Textarea(attrs={'placeholder' : 'Session Description'}))
    hour_count = forms.DecimalField(label='number of hours', widget=forms.NumberInput(attrs={'placeholder' : 'Number of Hours'}))
    difficulty = forms.IntegerField(label= 'difficulty level')


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