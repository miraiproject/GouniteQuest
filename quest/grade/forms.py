from django.forms import ModelForm
from .models import Grade


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['english', 'math', 'japanese']
