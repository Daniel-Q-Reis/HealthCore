from django.http import HttpRequest, HttpResponse
from django.conf import settings
from health_check.plugins import plugin_dir
from health_check.views import MainView
from typing import Any


def liveness_probe(request: HttpRequest) -> HttpResponse:
    """
    Liveness probe endpoint.

    Returns a 200 OK response to indicate that the application process is running.
    This check does not verify dependency health.
    """
    return HttpResponse("OK")


class ReadinessProbeView(MainView):  # type: ignore[misc]
    """
    Readiness probe endpoint.

    Inherits from django-health-check's main view and forces a JSON response.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        plugins = {}
        for plugin_class in plugin_dir._registry:
            if isinstance(plugin_class, tuple):
                # Handle plugins registered with arguments, e.g., CacheBackend
                cls, options = plugin_class
                plugin = cls(**options)
            else:
                # Handle plugins registered as a simple class
                plugin = plugin_class()
            plugins[plugin.identifier()] = plugin

        # Remove the generic 'DatabaseBackend' if more specific DB checks exist
        if "DatabaseBackend" in plugins and len(settings.DATABASES) > 0:
            plugins.pop("DatabaseBackend", None)

        for plugin in plugins.values():
            plugin.run_check()

        status = 503 if any(p.errors for p in plugins.values()) else 200

        response = self.render_to_response_json(plugins, status=status)
        return response  # type: ignore[no-any-return]
