from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("beheer/", admin.site.urls),
    path("admin/", RedirectView.as_view(pattern_name="admin:index", permanent=False)),
    path("", include("school.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
