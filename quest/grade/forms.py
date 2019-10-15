from django.forms import ModelForm
from .models import Grade, Board



class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['english', 'math', 'japanese']

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['comment', 'date']