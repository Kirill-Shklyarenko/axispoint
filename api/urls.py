from django.urls import include, path
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.views import APIView

from . import views


class DocsView(APIView):
    """
    RESTFul Documentation of my app
    """

    def get(self, request, *args, **kwargs):
        apidocs = {'View paginated data': request.build_absolute_uri('api/'),
                   'View all data in json': request.build_absolute_uri('json/'),
                   'Export all data to .xlsx': request.build_absolute_uri('xlsx/'),
                   }
        return Response(apidocs)


router = routers.DefaultRouter()
router.register('json', views.JSONListView)
router.register('xlsx', views.XLSXViewSet)


urlpatterns = [
    path('', DocsView.as_view()),
    path('', include(router.urls)),

    path('api/', views.APIListView.as_view(), name='api'),
    path('json/', views.JSONListView.as_view({'get': 'list'}), name='json'),
    path('xlsx/', views.XLSXViewSet.as_view({'get': 'list'}), name='xlsx'),

]
