from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('Export_to_XLSX', views.XLSXViewSet)

urlpatterns = [
    path('', views.APIListView.as_view(), name='all-letters'),
    path('XLSX/', include(router.urls)),

]
