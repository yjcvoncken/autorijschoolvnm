from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect


class RailwayHealthCheckMiddleware:
    """Answer Railway probes before redirects, host checks, or database access."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health/":
            return HttpResponse("ok")
        return self.get_response(request)


class CanonicalDomainMiddleware:
    """Redirect the bare production domain to its canonical www address."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_host().split(":", 1)[0].lower() == "autorijschoolvnm.nl":
            return HttpResponsePermanentRedirect(
                f"https://www.autorijschoolvnm.nl{request.get_full_path()}"
            )
        return self.get_response(request)
