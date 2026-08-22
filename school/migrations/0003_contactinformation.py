from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("school", "0002_update_packages")]
    operations = [
        migrations.CreateModel(
            name="ContactInformation",
            fields=[],
            options={
                "verbose_name": "contactgegeven",
                "verbose_name_plural": "contactgegevens",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("school.sitesettings",),
        ),
    ]
