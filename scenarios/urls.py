from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScenarioViewSet, ExecutionViewSet

router = DefaultRouter()
router.register(r'scenarios', ScenarioViewSet)
router.register(r'executions', ExecutionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
