from datetime import timedelta

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.template.response import TemplateResponse
from django.utils import timezone

from .models import ContactInformation, ContactRequest, GalleryImage, Package, PageViewDaily, SiteSettings

admin.site.site_header = "Autorijschool VNM beheer"
admin.site.site_title = "VNM beheer"
admin.site.index_title = "Website beheren"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = ("hero_title", "hero_text", "about_title", "about_text", "instructor", "success_rate")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    fields = (
        "phone", "email", "notification_email", "address", "city", "whatsapp",
        "facebook_url", "instagram_url",
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "featured", "active", "order")
    list_editable = ("featured", "active", "order")
    search_fields = ("name", "description")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "order")
    list_editable = ("active", "order")


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "package", "subject", "created_at", "handled")
    list_filter = ("handled", "subject", "created_at")
    list_editable = ("handled",)
    search_fields = ("name", "phone", "email", "message")
    readonly_fields = ("name", "phone", "email", "package", "subject", "message", "created_at")


@admin.register(PageViewDaily)
class AnalyticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/school/analytics.html"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        try:
            days = int(request.GET.get("days", 30))
        except (TypeError, ValueError):
            days = 30
        if days not in (7, 30, 90):
            days = 30
        today = timezone.localdate()
        start = today - timedelta(days=days - 1)
        views = PageViewDaily.objects.filter(date__range=(start, today))
        contacts = ContactRequest.objects.filter(
            created_at__date__range=(start, today),
        )
        daily = dict(views.values("date").annotate(total=Sum("views")).values_list("date", "total"))
        timeline = [{"date": start + timedelta(days=i), "views": daily.get(start + timedelta(days=i), 0)} for i in range(days)]
        maximum = max((row["views"] for row in timeline), default=0)
        for row in timeline:
            row["width"] = round(row["views"] / maximum * 100) if maximum else 0
        context = {
            **self.admin_site.each_context(request),
            "title": "Website analytics", "opts": self.model._meta,
            "days": days, "periods": (7, 30, 90), "start": start, "today": today,
            "total_views": views.aggregate(total=Sum("views"))["total"] or 0,
            "total_contacts": contacts.count(),
            "pages": views.values("path").annotate(total=Sum("views")).order_by("-total"),
            "timeline": timeline,
        }
        if not self.has_view_permission(request):
            raise PermissionDenied
        return TemplateResponse(request, self.change_list_template, context)
