from django import forms
from .models import Employee,Team

class loginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Employee
        fields=['username','password']

class registerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Employee
        fields=['username','password','employee_Team','employee_role']
    employee_Team = forms.ModelChoiceField(queryset= Team.objects.all(),empty_label=None)

