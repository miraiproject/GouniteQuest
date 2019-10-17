from django.forms import ModelForm
from grade.models import Grade
from grade.models import Report
from grade.models import SubmittedReport
from grade.models import Board


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ["english", "math", "japanese"]


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["title", "content"]


class SubmittedReportForm(ModelForm):
    class Meta:
        model = SubmittedReport
        fields = ["submittion"]
        

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['comment'] 