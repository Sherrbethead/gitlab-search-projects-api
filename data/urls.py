from rest_framework.routers import DefaultRouter
from .views import SearchDataView

app_name = 'data'

# Wire up using automatic URL routing
router = DefaultRouter()
router.register('api', SearchDataView)
urlpatterns = router.urls
