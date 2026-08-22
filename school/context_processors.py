from .models import SiteSettings


def site_data(request):
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    return {"site": settings}
