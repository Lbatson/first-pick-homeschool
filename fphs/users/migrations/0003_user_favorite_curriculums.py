# Generated by Django 3.0.5 on 2020-07-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculums', '0011_auto_20200529_0234'),
        ('users', '0002_create_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_curriculums',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='curriculums.Curriculum'),
        ),
    ]
