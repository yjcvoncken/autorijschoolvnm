from django.contrib import admin
from .models import ContactInformation, ContactRequest, GalleryImage, Package, SiteSettings

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
