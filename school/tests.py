from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactRequest, Package, SiteSettings


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PublicWebsiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSettings.objects.create()
        Package.objects.create(
            name="Proefles", price="€ 49", description="Kennismaken",
            features="60 minuten rijles\nPersoonlijk advies",
        )

    def test_public_pages_load(self):
        for name in ("home", "about", "packages", "contact"):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_railway_healthcheck(self):
        response = self.client.get("/health/", headers={"host": "healthcheck.railway.app"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_contact_request_is_saved(self):
        package = Package.objects.get(name="Proefles")
        response = self.client.post(reverse("contact"), {
            "name": "Test Leerling",
            "phone": "0612345678",
            "email": "leerling@example.com",
            "package": package.pk,
            "subject": "proefles",
            "message": "Ik wil graag kennismaken.",
        })
        self.assertRedirects(response, reverse("contact"))
        self.assertTrue(ContactRequest.objects.filter(email="leerling@example.com").exists())
        self.assertEqual(ContactRequest.objects.get(email="leerling@example.com").package, package)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Pakket: Proefles", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].reply_to, ["leerling@example.com"])

    def test_package_query_parameter_preselects_package(self):
        package = Package.objects.get(name="Proefles")
        response = self.client.get(reverse("contact"), {"pakket": package.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'<option value="{package.pk}" selected>')

    def test_contact_page_links_phone_email_and_social_media(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response, 'href="tel:06-28868238"')
        self.assertContains(response, 'href="mailto:autorijschoolvnm1971@hotmail.com"')
        self.assertContains(response, "https://www.facebook.com/people/Autorijschool-Vnm/100078653213544/")
        self.assertContains(response, "https://www.instagram.com/autorijschoolvnm/")


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            username="admin-test",
            email="admin@example.com",
            password="test-password",
        )
        SiteSettings.objects.create()

    def test_admin_is_available_and_conventional_url_redirects(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get("/beheer/").status_code, 200)
        self.assertRedirects(self.client.get("/admin/"), "/beheer/")

    def test_site_settings_can_be_opened_in_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get("/beheer/school/sitesettings/1/change/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Samen op weg naar jouw rijbewijs!")
