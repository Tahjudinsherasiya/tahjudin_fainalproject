from django import forms
from .models import *

class signupform(forms.ModelForm):
    class Meta:
        model=signupdata
        fields='__all__'
        
class updateForm(forms.ModelForm):
    class Meta:
        model=signupdata
        fields=['firstname','lastname','username','password','city','state','mobile']

class notesForm(forms.ModelForm):
    class Meta:
        model=mynotes
        fields='__all__'
        
class feedbackform(forms.ModelForm):
    class Meta:
        model=feedback
        fields='__all__'