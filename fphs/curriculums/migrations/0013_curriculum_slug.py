from django.db import migrations, models
from django.utils.text import slugify

def generate_slug(apps, schema_editor):
    Curriculum = apps.get_model("curriculums", "Curriculum")
    for curriculum in Curriculum.objects.all():
        curriculum.slug = slugify(curriculum.name)
        curriculum.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("curriculums", "0012_curriculum_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="curriculum",
            name="slug",
            field=models.SlugField(max_length=200, db_index=False, null=True),
        ),
        migrations.RunPython(generate_slug),
        migrations.AlterField(
            model_name="curriculum",
            name="slug",
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
