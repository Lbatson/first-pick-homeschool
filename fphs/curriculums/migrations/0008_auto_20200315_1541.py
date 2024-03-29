# Generated by Django 3.0.1 on 2020-03-15 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("curriculums", "0007_auto_20200104_0331"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.AddField(
            model_name="curriculum",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="curriculums",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
