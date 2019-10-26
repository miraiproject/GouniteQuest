from django.urls import reverse, resolve
from django.test import Client, TestCase
from .views import signup, index
from .views_grade import new_grade, update_grade, show_grade
from .views_report import new_report_problem, update_report_problem, new_report
from .models import CustomUser, Grade, ReportProblem, Report
from .forms import GradeForm


def create_client_and_teacher_and_student(self):
    self.client = Client()
    self.teacher = CustomUser.objects.create(is_teacher=True)
    self.student = CustomUser.objects.create(username='student')


def test_only_teacher_can_access(self, url):
    # teacher -> 200
    self.client.force_login(self.teacher)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # logged out user -> 302
    self.client.logout()
    response = self.client.get(url)
    self.assertEqual(response.status_code, 302)

    # student -> 302
    self.client.force_login(self.student)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 302)


def test_logged_in_user_can_access(self, url):
    # teacher -> 200
    self.client.force_login(self.teacher)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # logged out user -> 302
    self.client.logout()
    response = self.client.get(url)
    self.assertEqual(response.status_code, 302)

    # student -> 200
    self.client.force_login(self.student)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


class SignUpTests(TestCase):

    def test_signup_view_status_code(self):
        url = reverse('grade:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)


class IndexTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)

    def test_index_view_status_code(self):
        url = reverse('grade:index')
        test_logged_in_user_can_access(self, url)

    def test_root_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEqual(view.func, index)

    def test_context(self):
        url = reverse('grade:index')

        self.client.force_login(self.student)
        response = self.client.get(url)
        self.assertEqual(None, response.context['grade'])
        self.assertEqual(0, response.context['reports'].count())
        self.assertEqual(0, response.context['submitted_problems'].count())
        self.assertEqual(0, response.context['not_submitted_problems'].count())

        grade = Grade.objects.create(
            english=21, math=32, japanese=7, gpa=20, user=self.student
        )
        report_problem = ReportProblem.objects.create(
            title="title", content="content", teacher=self.teacher
        )

        response = self.client.get(url)
        self.assertEqual(grade, response.context['grade'])
        self.assertEqual(1, response.context['not_submitted_problems'].count())

        Report.objects.create(
            report_file="test.jpg",
            report_problem=report_problem,
            student=self.student
        )

        response = self.client.get(url)
        self.assertEqual(1, response.context['reports'].count())
        self.assertEqual(1, response.context['submitted_problems'].count())
        self.assertEqual(0, response.context['not_submitted_problems'].count())

        self.client.force_login(self.teacher)
        response = self.client.get(url)
        self.assertEqual(1, response.context['report_problems'].count())
        self.assertEqual(1, response.context['reports'].count())


class NewGradeTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)

    def test_new_grade_view_status_code(self):
        url = reverse('grade:new_grade', args=[self.student.id])
        test_only_teacher_can_access(self, url)

    def test_new_grade_url_resolves_new_grade_view(self):
        view = resolve('/new_grade/%d/' % self.student.id)
        self.assertEqual(view.func, new_grade)

    def test_context(self):
        url = reverse('grade:new_grade', args=[self.student.id])

        self.client.force_login(self.teacher)
        response = self.client.get(url)
        self.assertEqual(self.student, response.context['user'])

    def test_grade_form(self):
        url = reverse('grade:new_grade', args=[self.student.id])
        form_data = {'english': 21, 'math': 32, 'japanese': 13}
        form = GradeForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.client.force_login(self.teacher)
        self.assertEqual(0, Grade.objects.all().count())
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, Grade.objects.all().count())
        self.assertEqual(22.0, Grade.objects.all().first().gpa)


class UpdateGradeTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.grade = Grade.objects.create(
            english=36, math=24, japanese=12, gpa=24, user=self.student
        )

    def test_update_grade_view_status_code(self):
        url = reverse('grade:update_grade', args=[self.student.id])
        test_only_teacher_can_access(self, url)

    def test_update_grade_url_resolves_update_grade_view(self):
        view = resolve('/update_grade/%d/' % self.student.id)
        self.assertEqual(view.func, update_grade)


class ShowGradeTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)

    def test_show_grade_view_status_code(self):
        url = reverse('grade:show_grade')
        test_only_teacher_can_access(self, url)

    def test_show_grade_url_resolves_show_grade_view(self):
        view = resolve('/show_grade/')
        self.assertEqual(view.func, show_grade)


class NewReportProblemTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)

    def test_new_report_problem_view_status_code(self):
        url = reverse('grade:new_report_problem')
        test_only_teacher_can_access(self, url)

    def test_new_report_problem_url_resolves_new_report_problem_view(self):
        view = resolve('/new_report_problem/')
        self.assertEqual(view.func, new_report_problem)


class UpdateReportProblemTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.report_problem = ReportProblem.objects.create(
            title='title', content='content', teacher=self.teacher
        )

    def test_update_report_problem_view_status_code(self):
        url = reverse('grade:update_report_problem',
                      args=[self.report_problem.id])
        test_only_teacher_can_access(self, url)

    def test_update_report_problem_url_resolves_update_report_problem_view(
            self):
        view = resolve('/update_report_problem/%d/' % self.report_problem.id)
        self.assertEqual(view.func, update_report_problem)


class NewReportTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.report_problem = ReportProblem.objects.create(
            title='title', content='content', teacher=self.teacher
        )

    def test_new_report_view_status_code(self):
        url = reverse('grade:new_report', args=[self.report_problem.id])
        test_logged_in_user_can_access(self, url)

    def test_new_report_url_resolves_new_report_view(self):
        view = resolve('/new_report/%d/' % self.report_problem.id)
        self.assertEqual(view.func, new_report)


class CustomUserModelTest(TestCase):

    def test_culumn(self):
        user = CustomUser.objects.create(
            username='name',
            email="test@exmaple.com"
        )
        self.assertEqual(user.username, 'name')
        self.assertEqual(user.email, "test@exmaple.com")
        self.assertEqual(str(user), user.username)
        self.assertFalse(user.is_teacher)
        user.is_teacher = True
        self.assertTrue(user.is_teacher)
