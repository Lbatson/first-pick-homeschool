from django.db import migrations, models
import uuid

def generate_uuid(apps, schema_editor):
    Review = apps.get_model("curriculums", "Review")
    for review in Review.objects.all():
        review.uuid = uuid.uuid4()
        review.save(update_fields=["uuid"])


class Migration(migrations.Migration):

    dependencies = [
        ("curriculums", "0013_curriculum_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generate_uuid),
        migrations.AlterField(
            model_name="review",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        )
    ]
