from django.urls import path

from . import views

app_name = 'axis'

urlpatterns = [
    path('', views.save_to_model, name='download'),
]
