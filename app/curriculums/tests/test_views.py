from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from curriculums.models import (
    Category,
    Subject,
    Grade,
    Level,
    Age,
    Publisher,
    Curriculum
)


class CurriculumIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='TestCategory')
        subject = Subject.objects.create(name='TestSubject', category=category)
        grade = Grade.objects.create(name='TestGrade')
        level = Level.objects.create(name='TestLevel')
        age = Age.objects.create(name='999')
        publisher = Publisher.objects.create(name='TestPublisher')
        user = get_user_model().objects.create_user(
            email='Test@test.test',
            username='TestUser',
            password='TestPassword'
        )
        user.save()
        curriculum = Curriculum.objects.create(
            name='TestCurriculum',
            description='TestDescription',
            link='http://localhost',
            publisher=publisher,
            created_by=user
        )
        curriculum.subjects.add(subject)
        curriculum.grades.add(grade)
        curriculum.levels.add(level)
        curriculum.ages.add(age)

    def test_view_curriculums_url_settings_and_template(self):
        response = self.client.get('/curriculums/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('curriculums:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'curriculums/index.html') 

    def test_view_curriculums_lists_all(self):
        response = self.client.get(reverse('curriculums:index'))
        self.assertEqual(response.status_code, 200)
        curriculum = Curriculum.objects.get(name='TestCurriculum')
        self.assertEqual(list(response.context['curriculums']), [curriculum])
