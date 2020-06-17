from django import forms

class SessionAdd(forms.Form):
    #milestone = on the template page
    hour_count = forms.DecimalField(label='number of hours')
    difficulty = forms.IntegerField(min_value=1, max_value=5)
