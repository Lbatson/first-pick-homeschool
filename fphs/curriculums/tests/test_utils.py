from django.contrib.auth import get_user_model

from fphs.curriculums.models import (
    Category,
    Subject,
    Grade,
    Age,
    ReligiousPreference,
    Publisher,
    Curriculum,
)


def create_curriculum(name):
    category = Category.objects.create(name=name)
    subject = Subject.objects.create(name=name, category=category)
    grade = Grade.objects.create(name=name)
    age = Age.objects.create(name=name)
    religious_preference = ReligiousPreference.objects.create(name=name)
    publisher = Publisher.objects.create(name=name)
    user = get_user_model().objects.create_user(
        email="test@test.test", username=f"username{name}", password=f"password{name}"
    )
    user.save()
    curriculum = Curriculum.objects.create(
        name=name,
        description="description",
        link="http://localhost",
        religious_preference=religious_preference,
        publisher=publisher,
        created_by=user,
    )
    curriculum.subjects.add(subject)
    curriculum.grades.add(grade)
    curriculum.ages.add(age)
    return curriculum
