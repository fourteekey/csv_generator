from drf_yasg import openapi
from .serializers import *


error_schema = openapi.Schema(type=openapi.TYPE_OBJECT,
                              properties={'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message')})
url_schema = openapi.Schema(type=openapi.TYPE_OBJECT,
                            properties={'url': openapi.Schema(type=openapi.TYPE_STRING, description='url to dataset page')})

user_schema_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'ColumnSeparator': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'StringCharacter': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'columns': openapi.Schema(type=openapi.TYPE_OBJECT,
                                                  properties={'Order': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                              'ColumnName': openapi.Schema(type=openapi.TYPE_STRING),
                                                              'ColumnType': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                              'MinInteger': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                              'MaxInteger': openapi.Schema(type=openapi.TYPE_INTEGER)})
            })
