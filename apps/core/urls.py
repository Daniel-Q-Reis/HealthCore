from django.urls import path

from .views import ReadinessProbeView, liveness_probe

app_name = "core"

urlpatterns = [
    path("live", liveness_probe, name="liveness-probe"),
    path("ready", ReadinessProbeView.as_view(), name="readiness-probe"),
]
