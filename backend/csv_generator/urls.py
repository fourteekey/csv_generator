from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.index_view, name='index'),
    path('schema/new/', views.new_schema_view, name='new_schema'),
    path('schema/edit/<int:schema_id>/', views.edit_schema_view, name='edit_schema'),

    path('datasets/<int:schema_id>/', views.data_sets_view, name='datasets'),
    path('download/dataset/<int:dataset_id>', views.download_dataset, name='download_dataset'),

]
