from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('json', views.JSONListView)
router.register('xlsx', views.XLSXViewSet)

urlpatterns = [
    path('', views.DocsView.as_view()),
    path('', include(router.urls)),

    path('api/json/', views.JSONListView.as_view({'get': 'list'}), name='json'),
    path('api/xlsx/', views.XLSXViewSet.as_view({'get': 'list'}), name='xlsx'),
    path('api/paginated_data/', views.APIListView.as_view(), name='api'),

]
