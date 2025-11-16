# forms.py

from django import forms
from .models import *

class SignupForm(forms.ModelForm):
    class Meta:
        model = stu_details
        fields = ['name', 'age', 'div', 'enroll', 'stu_pass', 'email', 'roll_no', 'course_id']

class teachform(forms.ModelForm):
    class Meta:
        model =Registration_t 
        fields = '__all__'
