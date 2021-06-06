from django.urls import path
from . import views


urlpatterns = [
    path('schema', views.SchemaAPIView.as_view(), name='schema'),
    path('dataset', views.DataSetAPIView.as_view(), name='dataset'),
]
