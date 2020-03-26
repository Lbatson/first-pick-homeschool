from django.test import TestCase
from django.urls import reverse

from .test_utils import create_curriculum
from curriculums.urls import app_name
from curriculums.models import Curriculum


class CurriculumIndexViewTest(TestCase):
    ID = 1

    @classmethod
    def setUpTestData(cls):
        create_curriculum(CurriculumIndexViewTest.ID)

    def test_view_curriculums_url_settings_and_template(self):
        response = self.client.get(f'/{app_name}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(f'{app_name}:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{app_name}/index.html')

    def test_view_curriculums_lists_all(self):
        response = self.client.get(reverse(f'{app_name}:index'))
        self.assertEqual(response.status_code, 200)
        curriculum = Curriculum.objects.get(name=CurriculumIndexViewTest.ID)
        self.assertEqual(list(response.context[app_name]), [curriculum])
