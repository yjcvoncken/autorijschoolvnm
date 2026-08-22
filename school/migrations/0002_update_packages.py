from django.db import migrations


def update_packages(apps, schema_editor):
    Package = apps.get_model("school", "Package")
    packages = [
        ("Pakket A", "€ 1.000", "Voordelig starten", "Een compact lespakket inclusief praktijkexamen.", "10 rijlessen\nPraktijkexamen inbegrepen", False, 1),
        ("Pakket B", "€ 1.650", "Meest gekozen", "Een compleet lespakket met extra tijd om je rijvaardigheid op te bouwen.", "20 rijlessen\nPraktijkexamen inbegrepen", True, 2),
        ("Pakket C", "€ 2.300", "Uitgebreid", "Uitgebreide begeleiding vanaf de eerste les tot aan het praktijkexamen.", "30 rijlessen\nPraktijkexamen inbegrepen", False, 3),
        ("Losse rijles", "€ 70", "Per rijles", "Boek een losse rijles zonder lespakket.", "Eén losse rijles", False, 4),
        ("Praktijkexamen", "€ 350", "Examen", "Aanvraag en begeleiding bij het reguliere praktijkexamen.", "Praktijkexamen", False, 5),
        ("Faalangstexamen", "€ 350", "Extra begeleiding", "Een praktijkexamen met extra tijd en aandacht voor examenspanning.", "Faalangstexamen", False, 6),
        ("BNOR-examen", "€ 375", "Nader onderzoek", "Begeleiding en aanvraag van een BNOR-examen.", "BNOR-examen", False, 7),
        ("Tussentijdse toets", "€ 350", "Voorbereiding", "Ervaar alvast hoe een praktijkexamen verloopt en ontvang gericht advies.", "Tussentijdse toets", False, 8),
    ]
    Package.objects.all().delete()
    Package.objects.bulk_create([
        Package(name=name, price=price, label=label, description=description, features=features, featured=featured, order=order, active=True)
        for name, price, label, description, features, featured, order in packages
    ])


class Migration(migrations.Migration):
    dependencies = [("school", "0001_initial")]
    operations = [migrations.RunPython(update_packages, migrations.RunPython.noop)]
