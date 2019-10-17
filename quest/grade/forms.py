from django.forms import ModelForm
from grade.models import Grade
from grade.models import Report
<<<<<<< HEAD
from grade.models import ReportProblem
=======
from grade.models import SubmittedReport
from grade.models import Board
>>>>>>> ffa70ac4654a57248605e571438f2f9fad70374f


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ["english", "math", "japanese"]


class ReportProblemForm(ModelForm):
    class Meta:
        model = ReportProblem
        fields = ["title", "content"]


class ReportForm(ModelForm):
    class Meta:
        model = SubmittedReport
        fields = ["submittion"]


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['comment']
