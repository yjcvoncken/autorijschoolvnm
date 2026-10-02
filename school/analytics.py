import logging

from django.db import DatabaseError
from django.db.models import F
from django.utils import timezone

from .models import PageViewDaily

logger = logging.getLogger(__name__)


class PageViewMiddleware:
    """Count public page views without storing visitor identifiers."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        match = request.resolver_match
        if (request.method == "GET" and response.status_code == 200 and match
                and match.url_name in {"home", "about", "packages", "contact"}
                and not request.user.is_staff
                and not any(bot in request.META.get("HTTP_USER_AGENT", "").lower()
                            for bot in ("bot", "crawler", "spider", "headless"))):
            try:
                row, _ = PageViewDaily.objects.get_or_create(
                    date=timezone.localdate(), path=request.path,
                )
                PageViewDaily.objects.filter(pk=row.pk).update(views=F("views") + 1)
            except DatabaseError:
                logger.exception("Paginaweergave kon niet worden geteld")
        return response
