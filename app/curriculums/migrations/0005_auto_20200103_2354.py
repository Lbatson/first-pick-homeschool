# Generated by Django 3.0.1 on 2020-01-03 23:54

from django.db import migrations


def create_publishers(apps, schema_editor):
    Publisher = apps.get_model('curriculums', 'Publisher')
    Curriculum = apps.get_model('curriculums', 'Curriculum')

    for curriculum in Curriculum.objects.all():
        instance, _ = Publisher.objects.get_or_create(
            name="Default",
            link="http://127.0.0.1"
        )
        curriculum.publisher = instance
        curriculum.save()


class Migration(migrations.Migration):

    dependencies = [
        ('curriculums', '0004_auto_20200103_2349'),
    ]

    operations = [
        migrations.RunPython(create_publishers)
    ]
