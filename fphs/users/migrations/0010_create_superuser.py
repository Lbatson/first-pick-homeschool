from config.settings.base import ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD
from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(apps, schema_editor):
    superuser = get_user_model().objects.create_superuser(
        email=ADMIN_EMAIL, username=ADMIN_USERNAME, password=ADMIN_PASSWORD
    )

    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_remove_user_occupation"),
    ]

    operations = [migrations.RunPython(create_superuser)]
