from django.urls import path
from .views import SearchDataView


urlpatterns = [
    path('api/', SearchDataView.as_view()),
]
