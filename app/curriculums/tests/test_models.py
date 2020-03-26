from django.contrib.auth import get_user_model
from django.test import TestCase

from curriculums.models import (
    Category,
    Subject,
    Grade,
    Level,
    Age,
    Publisher,
    Curriculum
)


class CurriculumModelsTest(TestCase):
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

    def test_model_category(self):
        category = Category.objects.get(name='TestCategory')

        self.assertIsInstance(category, Category)
        self.assertEquals(category._meta.verbose_name, 'Category')
        self.assertEquals(category._meta.verbose_name_plural, 'Categories')

    def test_model_subject(self):
        category = Category.objects.get(name='TestCategory')
        subject = Subject.objects.get(name='TestSubject')

        self.assertIsInstance(subject, Subject)
        self.assertEquals(subject.category, category)

    def test_model_curriculum(self):
        curriculum = Curriculum.objects.get(name='TestCurriculum')
        subject = Subject.objects.get(name='TestSubject')
        grade = Grade.objects.get(name='TestGrade')
        level = Level.objects.get(name='TestLevel')
        age = Age.objects.get(name='999')
        publisher = Publisher.objects.get(name='TestPublisher')
        user = get_user_model().objects.get(username='TestUser')

        self.assertIsInstance(curriculum, Curriculum)
        self.assertEquals(curriculum.is_confirmed, False)
        self.assertEquals(list(curriculum.subjects.all()), [subject])
        self.assertEquals(list(curriculum.grades.all()), [grade])
        self.assertEquals(list(curriculum.levels.all()), [level])
        self.assertEquals(list(curriculum.ages.all()), [age])
        self.assertEquals(curriculum.price, 0.00)
        self.assertEquals(curriculum.subscription, False)
        self.assertEquals(curriculum.format, None)
        self.assertEquals(curriculum.consumable, None)
        self.assertEquals(curriculum.publisher, publisher)
        self.assertEquals(curriculum.created_by, user)
