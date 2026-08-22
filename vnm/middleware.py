from django.http import HttpResponse


class RailwayHealthCheckMiddleware:
    """Answer Railway probes before redirects, host checks, or database access."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health/":
            return HttpResponse("ok")
        return self.get_response(request)
