from django.http import HttpResponse
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics, response
from rest_framework.decorators import api_view, action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import LettersSerializer
from drf_renderer_xlsx.mixins import XLSXFileMixin
from axis.models import Letters


class APIListView(generics.ListAPIView):
    """
       Returns a list of all **letters** paginated and sorted by date.

       """
    queryset = Letters.objects.all().order_by('-date')
    serializer_class = LettersSerializer


class XLSXViewSet(XLSXFileMixin, ModelViewSet):
    queryset = Letters.objects.all().order_by('-date')
    serializer_class = LettersSerializer
    http_method_names = 'get'

    def get_renderers(self):
        if self.action == "export":
            return [XLSXRenderer()]
        else:
            return super().get_renderers()

    @action(methods=["GET"], detail=False)
    def export(self, request: Request) -> Response:
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

    def get_row_color(self, obj) -> str:
        """
        This method returns color value for row in XLSX sheet.
        (*self.instance,) extends queryset to a list (it must be a queryset, not a single Endpoint).
        .index(obj) gets index of currently serialized object in that list.
        As the last step one out of two values from the list is chosen using modulo 2 operation on the index.
        """
        return ["353535", "2B2B2B"][(*self.instance,).index(obj) % 2]
