from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("school", "0005_update_contact_email")]
    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="notification_email",
            field=models.EmailField(
                blank=True,
                help_text="Bijvoorbeeld je Gmail-adres. Leeg laten om het openbare e-mailadres te gebruiken.",
                max_length=254,
                verbose_name="ontvangstadres formulieren",
            ),
        ),
    ]
