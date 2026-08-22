from django.db import migrations, models


def update_email(apps, schema_editor):
    SiteSettings = apps.get_model("school", "SiteSettings")
    SiteSettings.objects.update(email="autorijschoolvnm1971@hotmail.com")


class Migration(migrations.Migration):
    dependencies = [("school", "0004_contactrequest_package")]
    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="email",
            field=models.EmailField(
                default="autorijschoolvnm1971@hotmail.com",
                max_length=254,
                verbose_name="e-mailadres",
            ),
        ),
        migrations.RunPython(update_email, migrations.RunPython.noop),
    ]
