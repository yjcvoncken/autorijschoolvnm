import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactRequestForm
from .models import GalleryImage, Package, SiteSettings

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "school/home.html", {
        "packages": Package.objects.filter(active=True)[:3],
        "gallery": GalleryImage.objects.filter(active=True)[:4],
    })


def about(request):
    return render(request, "school/about.html", {"gallery": GalleryImage.objects.filter(active=True)})


def packages(request):
    return render(request, "school/packages.html", {"packages": Package.objects.filter(active=True)})


def contact(request):
    initial = {}
    if request.method == "GET" and request.GET.get("pakket"):
        selected_package = Package.objects.filter(pk=request.GET["pakket"], active=True).first()
        if selected_package:
            initial["package"] = selected_package
    form = ContactRequestForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        contact_request = form.save()
        site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
        recipient = (
            site_settings.notification_email
            or settings.CONTACT_RECIPIENT_EMAIL
            or site_settings.email
        )
        package_name = contact_request.package.name if contact_request.package else "Geen pakket gekozen"
        body = (
            "Er is een nieuwe aanvraag via de website binnengekomen.\n\n"
            f"Naam: {contact_request.name}\n"
            f"Telefoon: {contact_request.phone}\n"
            f"E-mail: {contact_request.email}\n"
            f"Pakket: {package_name}\n"
            f"Onderwerp: {contact_request.get_subject_display()}\n\n"
            f"Bericht:\n{contact_request.message or '-'}\n"
        )
        try:
            EmailMessage(
                subject=f"Nieuwe websiteaanvraag van {contact_request.name}",
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient],
                reply_to=[contact_request.email],
            ).send(fail_silently=False)
        except Exception:
            # De aanvraag blijft veilig in Django Admin staan als SMTP tijdelijk
            # niet bereikbaar is.
            logger.exception("Contactaanvraag %s kon niet worden gemaild", contact_request.pk)
        messages.success(request, "Bedankt! Je aanvraag is ontvangen. We nemen snel contact met je op.")
        return redirect("contact")
    return render(request, "school/contact.html", {"form": form})
