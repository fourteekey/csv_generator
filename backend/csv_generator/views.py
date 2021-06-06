import os

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import services
from .custom_schemas import *


def auth_view(request):
    if request.user.is_anonymous and request.POST:
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'error': 'Invalid login or password.'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def index_view(request):
    if not request.user.is_anonymous:
        return render(request, 'index.html', {'schemas': services.get_user_schemas(request.user),
                                              'username': request.user.username})

    return redirect('login')


def new_schema_view(request):
    if not request.user.is_anonymous:
        return render(request, 'schema.html', {'column_separators': services.get_column_separator(),
                                               'column_types': services.get_column_type(),
                                               'string_characters': services.get_string_character(),
                                               'username': request.user.username})
    return redirect('login')


def edit_schema_view(request, schema_id):
    if not request.user.is_anonymous:
        schema = services.get_user_detail_schema_by_id(request.user, schema_id)
        if not schema: return Response(status=status.HTTP_404_NOT_FOUND)

        return render(request, 'schema.html', {'column_separators': services.get_column_separator(),
                                               'column_types': services.get_column_type(),
                                               'string_characters': services.get_string_character(),
                                               'schema': schema,
                                               'username': request.user.username})
    return redirect('login')


def data_sets_view(request, schema_id):
    if not request.user.is_anonymous:
        # schema_id = request.query.schema_id
        return render(request, 'data_sets.html',
                      {'datasets': services.get_datasets(user=request.user, schema_id=schema_id),
                       'username': request.user.username,
                       'schema_id': schema_id})
    return redirect('login')


def download_dataset(request, dataset_id):
    dataset = services.get_dataset_by_idQuerySet(request.user, dataset_id)
    if dataset:
        filepath = settings.MEDIA_ROOT + dataset.filepath
        if os.path.exists(filepath):
            with open(filepath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = f'inline; filename={dataset.schema.filename}.csv'
                return response

    HTTP_REFERER = request.META['HTTP_REFERER']
    return redirect(HTTP_REFERER)


class SchemaAPIView(APIView):
    @swagger_auto_schema(
        operation_description='Create schema',
        request_body=user_schema_schema,
        responses={200: url_schema, 400: error_schema})
    def post(self, request):
        filename = request.data.get('FileName', None)
        column_separator = request.data.get('ColumnSeparator', None)
        string_character = request.data.get('StringCharacter', None)
        columns = request.data.get('columns', None)

        if not filename or not column_separator or not string_character or not columns:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        schema = services.create_schema(user=request.user,
                                        filename=filename,
                                        column_separator_id=column_separator,
                                        string_character_id=string_character)
        if not schema: return Response({'detail': 'Invalid string_character or column_separator'},
                                       status=status.HTTP_400_BAD_REQUEST)

        column_error = services.add_columns_to_schema(schema, columns)
        if column_error:
            services.delete_schema(schema)
            return Response({'detail': f'Cannot add columns to schema. {column_error}'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'url': reverse('datasets', kwargs={"schema_id": schema.id})})

    @swagger_auto_schema(
        operation_description='Update schema',
        manual_parameters=[openapi.Parameter('schema', openapi.IN_QUERY, type='number', required=True)],
        request_body=user_schema_schema,
        responses={200: url_schema, 400: error_schema}
    )
    def patch(self, request):
        schema_id = request.query_params.get('schema_id', None)
        schema = services.get_user_schema_by_idQuerySet(request.user, schema_id)
        if not schema: return Response({'detail': 'Invalid schema id.'}, status=status.HTTP_400_BAD_REQUEST)

        file_name = request.data.get('FileName', None)
        column_separator_id = request.data.get('ColumnSeparator', None)
        string_character_id = request.data.get('StringCharacter', None)
        columns = request.data.get('columns', None)

        schema_error = services.update_schema(schema=schema,
                                              filename=file_name,
                                              column_separator_id=column_separator_id,
                                              string_character_id=string_character_id)
        if schema_error: return Response({'detail': schema_error}, status=status.HTTP_400_BAD_REQUEST)

        services.delete_schema_columns(schema)
        column_error = services.add_columns_to_schema(schema, columns)
        if column_error: return Response({'detail': column_error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'url': reverse('datasets', kwargs={"schema_id": schema.id})})

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('schema', openapi.IN_QUERY, type='number', required=True)],
        responses={200: '', 400: error_schema})
    def delete(self, request):
        schema_id = request.query_params.get('schema', None)
        if not schema_id: return Response({'detail': 'Invalid schema id'}, status=status.HTTP_400_BAD_REQUEST)
        schema = services.get_user_schema_by_idQuerySet(request.user, schema_id)
        services.delete_schema(schema)
        return Response()


class DataSetAPIView(APIView):
    @swagger_auto_schema(
        operation_description='Create dataset',
        manual_parameters=[openapi.Parameter('schema', openapi.IN_QUERY, type='number', required=True)],
        responses={200: DataSetSerializer, 400: error_schema})
    def post(self, request):
        schema_id = request.query_params.get('schema', None)
        count_rows = request.data.get('count_rows', 0)

        if not schema_id or not count_rows: return Response({'detail': 'Request without required params.'},
                                                            status=status.HTTP_400_BAD_REQUEST)

        try:
            count_rows = int(count_rows)
        except Exception:
            Response({'detail': '\'count_rows\' must be int.'}, status=status.HTTP_400_BAD_REQUEST)

        if int(count_rows) < 0 or int(count_rows) > 100000:
            return Response({'detail': 'System cannot create file more 100 000 rows.'},
                            status=status.HTTP_400_BAD_REQUEST)

        schema = services.get_user_schema_by_idQuerySet(request.user, schema_id)
        if not schema: return Response({'detail': 'Schema not found.'}, status=status.HTTP_400_BAD_REQUEST)

        datasets = services.generate_dataset_csv(schema, count_rows)
        return Response(datasets)
