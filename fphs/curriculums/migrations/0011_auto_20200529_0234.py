# Generated by Django 3.0.1 on 2020-05-29 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("curriculums", "0010_auto_20200529_0201"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReligiousPreference",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name="curriculum",
            name="religious_preference",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="curriculums",
                to="curriculums.ReligiousPreference",
            ),
        ),
    ]
