from django import forms
from .models import TeacherModel

class TeacherModelForm(forms.ModelForm):
    class Meta:
        model = TeacherModel
        fields = '__all__' 