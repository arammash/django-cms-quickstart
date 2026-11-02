from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exhibitions", "0003_alter_artist_options_project_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="location",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
