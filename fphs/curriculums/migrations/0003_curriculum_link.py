# Generated by Django 3.0.1 on 2019-12-28 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("curriculums", "0002_auto_20191225_0321"),
    ]

    operations = [
        migrations.AddField(
            model_name="curriculum",
            name="link",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
    ]
