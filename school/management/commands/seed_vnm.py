from django.core.management.base import BaseCommand
from school.models import GalleryImage, Package, SiteSettings


class Command(BaseCommand):
    help = "Voegt de initiële VNM-inhoud toe"

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(pk=1)
        packages = [
            {"name": "Pakket A", "price": "€ 1.000", "label": "Voordelig starten", "description": "Een compact lespakket inclusief praktijkexamen.", "features": "10 rijlessen\nPraktijkexamen inbegrepen", "order": 1},
            {"name": "Pakket B", "price": "€ 1.650", "label": "Meest gekozen", "description": "Een compleet lespakket met extra tijd om je rijvaardigheid op te bouwen.", "features": "20 rijlessen\nPraktijkexamen inbegrepen", "featured": True, "order": 2},
            {"name": "Pakket C", "price": "€ 2.300", "label": "Uitgebreid", "description": "Uitgebreide begeleiding vanaf de eerste les tot aan het praktijkexamen.", "features": "30 rijlessen\nPraktijkexamen inbegrepen", "order": 3},
            {"name": "Losse rijles", "price": "€ 70", "label": "Per rijles", "description": "Boek een losse rijles zonder lespakket.", "features": "Eén losse rijles", "order": 4},
            {"name": "Praktijkexamen", "price": "€ 350", "label": "Examen", "description": "Aanvraag en begeleiding bij het reguliere praktijkexamen.", "features": "Praktijkexamen", "order": 5},
            {"name": "Faalangstexamen", "price": "€ 350", "label": "Extra begeleiding", "description": "Een praktijkexamen met extra tijd en aandacht voor examenspanning.", "features": "Faalangstexamen", "order": 6},
            {"name": "BNOR-examen", "price": "€ 375", "label": "Nader onderzoek", "description": "Begeleiding en aanvraag van een BNOR-examen.", "features": "BNOR-examen", "order": 7},
            {"name": "Tussentijdse toets", "price": "€ 350", "label": "Voorbereiding", "description": "Ervaar alvast hoe een praktijkexamen verloopt en ontvang gericht advies.", "features": "Tussentijdse toets", "order": 8},
        ]
        package_names = [package["name"] for package in packages]
        Package.objects.exclude(name__in=package_names).delete()
        for package in packages:
            name = package.pop("name")
            Package.objects.update_or_create(name=name, defaults=package)
        photos = [
            ("VNM banner", "gallery/vnm-banner.jpeg"),
            ("Lesauto", "gallery/car-sign.jpeg"),
            ("Visitekaart", "gallery/business-card.jpeg"),
            ("VNM impressie", "gallery/storyboard.jpeg"),
        ]
        for order, (title, image) in enumerate(photos, 1):
            GalleryImage.objects.get_or_create(title=title, defaults={"image": image, "alt_text": title, "order": order})
        self.stdout.write(self.style.SUCCESS("VNM-startinhoud is toegevoegd."))
