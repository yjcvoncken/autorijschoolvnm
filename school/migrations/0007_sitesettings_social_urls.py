from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("school", "0006_sitesettings_notification_email")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="facebook_url",
            field=models.URLField(
                blank=True,
                default="https://www.facebook.com/autorijschoolvnm",
                verbose_name="Facebook-link",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="instagram_url",
            field=models.URLField(
                blank=True,
                default="https://www.instagram.com/autorijschoolvnm/",
                verbose_name="Instagram-link",
            ),
        ),
    ]
