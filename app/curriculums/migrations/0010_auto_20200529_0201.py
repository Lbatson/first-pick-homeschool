# Generated by Django 3.0.1 on 2020-05-29 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculums', '0009_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculum',
            name='consumable',
        ),
        migrations.RemoveField(
            model_name='curriculum',
            name='format',
        ),
        migrations.RemoveField(
            model_name='curriculum',
            name='levels',
        ),
        migrations.RemoveField(
            model_name='curriculum',
            name='price',
        ),
        migrations.RemoveField(
            model_name='curriculum',
            name='subscription',
        ),
        migrations.AddField(
            model_name='curriculum',
            name='religious_preference',
            field=models.CharField(choices=[('R', 'Religious'), ('N', 'Faith Neutral'), ('S', 'Secular')], max_length=1, null=True),
        ),
        migrations.DeleteModel(
            name='Level',
        ),
    ]