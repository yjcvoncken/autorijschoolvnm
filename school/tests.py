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

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_railway_healthcheck_bypasses_https_redirect(self):
        response = self.client.get("/health/", headers={"host": "healthcheck.railway.app"})
        self.assertEqual(response.status_code, 200)

    def test_bare_domain_redirects_to_www_and_preserves_request(self):
        response = self.client.get(
            "/contact/?pakket=2",
            headers={"host": "autorijschoolvnm.nl"},
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.url,
            "https://www.autorijschoolvnm.nl/contact/?pakket=2",
        )

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


class AnalyticsTests(TestCase):
    def test_counts_public_views_without_query_strings(self):
        from .models import PageViewDaily
        self.client.get('/?email=private@example.com')
        self.client.get('/')
        self.assertEqual(PageViewDaily.objects.get(path='/').views, 2)
        self.assertEqual(PageViewDaily.objects.count(), 1)

    def test_ignores_bots_errors_health_and_post_requests(self):
        from .models import PageViewDaily
        self.client.get('/', HTTP_USER_AGENT='Googlebot')
        self.client.get('/missing/')
        self.client.get('/health/')
        self.client.post('/contact/', {})
        self.assertFalse(PageViewDaily.objects.exists())

    def test_admin_dashboard_permissions_and_totals(self):
        from .models import PageViewDaily
        from django.utils import timezone
        from datetime import timedelta
        PageViewDaily.objects.create(date=timezone.localdate(), path='/', views=12)
        PageViewDaily.objects.create(date=timezone.localdate() - timedelta(days=40), path='/', views=5)
        url = reverse('admin:school_pageviewdaily_changelist')
        self.assertEqual(self.client.get(url).status_code, 302)
        admin = get_user_model().objects.create_superuser('analytics-admin', password='test-password')
        self.client.force_login(admin)
        self.client.get('/')
        self.assertEqual(PageViewDaily.objects.get(date=timezone.localdate()).views, 12)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['total_views'], 12)
        response = self.client.get(url, {'days': 90})
        self.assertEqual(response.context_data['total_views'], 17)
        self.assertEqual(self.client.get(url, {'days': 'invalid'}).status_code, 200)
        self.assertContains(self.client.get('/beheer/'), 'analytics')
