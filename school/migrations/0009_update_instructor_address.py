from django.db import migrations, models


def update_site_details(apps, schema_editor):
    SiteSettings = apps.get_model("school", "SiteSettings")
    SiteSettings.objects.filter(instructor="Yasser").update(instructor="Mazin")
    SiteSettings.objects.filter(
        address="Voorstenkamp 13-27, 6545 EP Nijmegen"
    ).update(address="De Voorstenkamp 13-27, 6545 EP Nijmegen")


class Migration(migrations.Migration):
    dependencies = [("school", "0008_update_facebook_url")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="instructor",
            field=models.CharField(default="Mazin", max_length=100, verbose_name="naam instructeur"),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address",
            field=models.CharField(
                default="De Voorstenkamp 13-27, 6545 EP Nijmegen",
                max_length=200,
                verbose_name="adres",
            ),
        ),
        migrations.RunPython(update_site_details, migrations.RunPython.noop),
    ]
