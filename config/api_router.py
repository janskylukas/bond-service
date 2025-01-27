from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from bond_service.core.api.views import BondViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("bonds", BondViewSet)


app_name = "api"
urlpatterns = router.urls
