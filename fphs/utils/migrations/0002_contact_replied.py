# Generated by Django 3.0.5 on 2020-06-23 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="replied",
            field=models.BooleanField(default=False),
        ),
    ]