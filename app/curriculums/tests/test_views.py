from django.test import TestCase
from django.urls import reverse

from .test_utils import create_curriculum
from curriculums.urls import app_name
from curriculums.models import Curriculum, Sort


class CurriculumIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            create_curriculum(i + 1)

    def test_view_curriculums_url_settings_and_template(self):
        response = self.client.get(f'/{app_name}/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse(f'{app_name}:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{app_name}/index.html')

    def test_view_curriculums_lists_all(self):
        response = self.client.get(f'/{app_name}/')
        curriculums = Curriculum.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[app_name]), 5)
        self.assertEqual(
            list(response.context[app_name]),
            list(curriculums.order_by(Sort.Values.NEWEST.label))
        )

    def test_view_curriculums_lists_filter_categories(self):
        curriculum = Curriculum.objects.get(name=1)
        category = curriculum.subjects.all().first().category.id
        response = self.client.get(f'/{app_name}/?category={category}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[app_name]), 1)
        self.assertEqual(list(response.context[app_name]), [curriculum])

    def test_view_curriculums_lists_filter_multiple_params(self):
        curriculum = Curriculum.objects.get(name=1)
        grade = curriculum.grades.all().first().id
        age = curriculum.ages.all().first().id
        response = self.client.get(
            f'/{app_name}/?grade={grade}&age={age}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[app_name]), 1)
        self.assertEqual(list(response.context[app_name]), [curriculum])

    def test_view_curriculums_lists_filter_multiple_values(self):
        curriculums = Curriculum.objects.all().order_by('id')
        grades = list(map(lambda x: x.grades.all().first().id, curriculums))[:4]
        query_string = '?' + '&'.join(list(map(lambda x: f'grade={x}', grades)))
        response = self.client.get(f'/{app_name}/{query_string}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[app_name]), 4)
        self.assertEqual(
            list(response.context[app_name]),
            list(curriculums.order_by(Sort.Values.NEWEST.label))[1:]
        )
