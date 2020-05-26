from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import LettersSerializer
from axis.models import Letters


class DocsView(APIView):
    """
    1) Need to download data from given URL and save to DataBase. WARNING! It’s a
    very long process, you need to wait ...
    2) For viewing data in json (EndPoint №1)
    3) For conver and export data .xlslxlls file (EndPoint №2)
    4) Just for confortable preview (paginated by 100 elements on the page)

    """

    def get(self, request, *args, **kwargs):
        apidocs = {'1)Download and Save data': request.build_absolute_uri('download/'),
                   '2)View all data in json': request.build_absolute_uri('api/json/'),
                   '3)Export all data to .xlsx': request.build_absolute_uri('api/xlsx/'),
                   '4)View paginated data': request.build_absolute_uri('api/paginated_data/'),
                   }
        return Response(apidocs)


class JSONListView(ReadOnlyModelViewSet):
    """
           Returns a JSON list of letters paginated and sorted by date.

    """
    queryset = Letters.objects.all().order_by('-date')
    serializer_class = LettersSerializer
    pagination_class = None

    def get_renderers(self):
        return [JSONRenderer()]

    def get_renderer_context(self):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response = Response(data=serializer.data, headers={'indent': '    '})
        return response


class XLSXViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """
           Export all data to .xlsx file

    """
    queryset = Letters.objects.all().order_by('-date')
    serializer_class = LettersSerializer
    pagination_class = None

    def get_renderers(self):
        return [XLSXRenderer()]

    @action(methods=["GET"], detail=False)
    def export_all_to_xlsx(self, request: Request) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    # Properties for XLSX
    column_header = {
        "titles": [
            "Id", "Category", "Sender", "Title", "Text", "Date"
        ],
        'column_width': [8, 12, 15, 20, 160, 15],
        'height': 50,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {
        'style': {
            'fill': {
                'fill_type': 'solid',
                # 'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': False,
                'color': 'FF000000',
            }
        },
        'height': 170,
    }


class APIListView(generics.ListAPIView):
    """
       Returns a paginated and sorted by date list of greetings .

    """
    queryset = Letters.objects.all().order_by('-date')
    serializer_class = LettersSerializer

    def get_renderers(self):
        return [BrowsableAPIRenderer(), JSONRenderer(), XLSXRenderer()]
