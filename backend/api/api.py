from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('csv_generator.api')),
]