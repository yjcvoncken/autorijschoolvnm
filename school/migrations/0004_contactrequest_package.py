import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("school", "0003_contactinformation")]
    operations = [
        migrations.AddField(
            model_name="contactrequest",
            name="package",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contact_requests",
                to="school.package",
                verbose_name="gekozen pakket",
            ),
        ),
    ]
