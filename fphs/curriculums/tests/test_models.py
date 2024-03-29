from django.contrib.auth import get_user_model
from django.test import TestCase

from .test_utils import create_curriculum
from fphs.curriculums.models import (
    Category,
    Subject,
    Grade,
    Age,
    ReligiousPreference,
    Publisher,
    Curriculum,
    Review,
)


class CurriculumModelsTest(TestCase):
    ID = 1

    @classmethod
    def setUpTestData(cls):
        create_curriculum(CurriculumModelsTest.ID)

    def test_model_category(self):
        category = Category.objects.get(name=CurriculumModelsTest.ID)

        self.assertIsInstance(category, Category)
        self.assertEquals(category._meta.verbose_name, "Category")
        self.assertEquals(category._meta.verbose_name_plural, "Categories")

    def test_model_subject(self):
        category = Category.objects.get(name=CurriculumModelsTest.ID)
        subject = Subject.objects.get(name=CurriculumModelsTest.ID)

        self.assertIsInstance(subject, Subject)
        self.assertEquals(subject.category, category)

    def test_model_curriculum(self):
        curriculum = Curriculum.objects.get(name=CurriculumModelsTest.ID)
        subject = Subject.objects.get(name=CurriculumModelsTest.ID)
        grade = Grade.objects.get(name=CurriculumModelsTest.ID)
        age = Age.objects.get(name=CurriculumModelsTest.ID)
        religious_preference = ReligiousPreference.objects.get(
            name=CurriculumModelsTest.ID
        )
        publisher = Publisher.objects.get(name=CurriculumModelsTest.ID)
        user = get_user_model().objects.get(
            username=f"username{CurriculumModelsTest.ID}"
        )

        self.assertIsInstance(curriculum, Curriculum)
        self.assertEquals(curriculum.is_confirmed, False)
        self.assertEquals(list(curriculum.subjects.all()), [subject])
        self.assertEquals(list(curriculum.grades.all()), [grade])
        self.assertEquals(list(curriculum.ages.all()), [age])
        self.assertEquals(curriculum.religious_preference, religious_preference)
        self.assertEquals(curriculum.publisher, publisher)
        self.assertEquals(curriculum.created_by, user)

    def test_model_review(self):
        name = "Test2"
        curriculum = Curriculum.objects.get(name=CurriculumModelsTest.ID)
        user = get_user_model().objects.create_user(
            email="test2@test.test",
            username=f"username{name}",
            password=f"password{name}",
        )
        user.save()
        review = Review.objects.create(
            curriculum=curriculum, content=name, rating=5, user=user
        )

        self.assertEqual(list(curriculum.reviews.all()), [review])
        self.assertEqual(list(user.reviews.all()), [review])
