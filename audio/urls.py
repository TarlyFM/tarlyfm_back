from .views import AudioViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'audio', AudioViewSet, base_name='audio')
urlpatterns = router.urls
