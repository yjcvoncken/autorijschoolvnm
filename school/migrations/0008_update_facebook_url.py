from django.db import migrations, models


OLD_URL = "https://www.facebook.com/autorijschoolvnm"
NEW_URL = "https://www.facebook.com/people/Autorijschool-Vnm/100078653213544/"


def update_facebook_url(apps, schema_editor):
    SiteSettings = apps.get_model("school", "SiteSettings")
    SiteSettings.objects.filter(facebook_url=OLD_URL).update(facebook_url=NEW_URL)


class Migration(migrations.Migration):
    dependencies = [("school", "0007_sitesettings_social_urls")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="facebook_url",
            field=models.URLField(blank=True, default=NEW_URL, verbose_name="Facebook-link"),
        ),
        migrations.RunPython(update_facebook_url, migrations.RunPython.noop),
    ]
