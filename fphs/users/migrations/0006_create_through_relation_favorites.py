from django.contrib.auth import get_user_model
from django.db import migrations

def create_through_relations(apps, schema_editor):
    User = get_user_model()
    FavoriteCurriculum = apps.get_model('users', 'FavoriteCurriculum')
    for user in User.objects.all():
        for curriculum in user.favorite_curriculums.all():
            FavoriteCurriculum(user=user, curriculum=curriculum).save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_favoritecurriculum'),
    ]

    operations = [migrations.RunPython(create_through_relations)]
