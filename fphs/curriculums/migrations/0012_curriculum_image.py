# Generated by Django 3.0.5 on 2020-07-29 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('curriculums', '0011_auto_20200529_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image'),
        ),
    ]
