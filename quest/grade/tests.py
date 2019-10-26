from django.urls import reverse, resolve
from django.test import Client, TestCase
from .views import signup, index
from .views_grade import new_grade, update_grade, show_grade
from .views_report import new_report_problem, update_report_problem, new_report
from .models import CustomUser, Grade, ReportProblem


def create_client_and_teacher_and_student(self):
    self.client = Client()
    self.teacher = CustomUser.objects.create(is_teacher=True)
    self.student = CustomUser.objects.create(username='student')


def test_only_teacher_can_access(self, url):
    # teacher -> 200
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
        self.client.force_login(self.teacher)

    def test_index_view_status_code(self):
        url = reverse('grade:index')
        test_logged_in_user_can_access(self, url)

    def test_root_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEqual(view.func, index)


class NewGradeTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.client.force_login(self.teacher)

    def test_new_grade_view_status_code(self):
        url = reverse('grade:new_grade', args=[1])
        test_only_teacher_can_access(self, url)

    def test_new_grade_url_resolves_new_grade_view(self):
        view = resolve('/new_grade/1/')
        self.assertEqual(view.func, new_grade)


class UpdateGradeTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.client.force_login(self.teacher)
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
        self.client.force_login(self.teacher)

    def test_show_grade_view_status_code(self):
        url = reverse('grade:show_grade')
        test_only_teacher_can_access(self, url)

    def test_show_grade_url_resolves_show_grade_view(self):
        view = resolve('/show_grade/')
        self.assertEqual(view.func, show_grade)


class NewReportProblemTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.client.force_login(self.teacher)

    def test_new_report_problem_view_status_code(self):
        url = reverse('grade:new_report_problem')
        test_only_teacher_can_access(self, url)

    def test_new_report_problem_url_resolves_new_report_problem_view(self):
        view = resolve('/new_report_problem/')
        self.assertEqual(view.func, new_report_problem)


class UpdateReportProblemTests(TestCase):

    def setUp(self):
        create_client_and_teacher_and_student(self)
        self.client.force_login(self.teacher)
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
        self.client.force_login(self.student)
        self.report_problem = ReportProblem.objects.create(
            title='title', content='content', teacher=self.teacher
        )

    def test_new_report_view_status_code(self):
        url = reverse('grade:new_report', args=[self.report_problem.id])
        test_logged_in_user_can_access(self, url)

    def test_new_report_url_resolves_new_report_view(self):
        view = resolve('/new_report/%d/' % self.report_problem.id)
        self.assertEqual(view.func, new_report)
