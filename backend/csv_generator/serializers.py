from rest_framework import serializers
from .models import *


class SchemaColumnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaColumns
        fields = '__all__'


class ColumnSeparatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnSeparator
        fields = '__all__'


class ColumnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnType
        fields = '__all__'


class StringCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringCharacter
        fields = '__all__'


class SchemaSerializer(serializers.ModelSerializer):
    modified = serializers.DateField(format="%Y-%d-%m", input_formats=('%d-%m-%Y',))

    class Meta:
        model = Schemas
        fields = ('id', 'filename', 'column_separator', 'string_character', 'modified')


class SchemaDetailSerializer(serializers.ModelSerializer):
    modified = serializers.DateField(format="%Y-%d-%m", input_formats=('%d-%m-%Y',))
    columns = serializers.SerializerMethodField()

    class Meta:
        model = Schemas
        fields = ('id', 'filename', 'column_separator', 'string_character', 'modified', 'columns')

    @staticmethod
    def get_columns(obj):
        columns = SchemaColumns.objects.filter(schema=obj)
        return SchemaColumnsSerializer(columns, many=True).data


class DataSetSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format="%Y-%d-%m", input_formats=('%d-%m-%Y',))
    status_id = serializers.IntegerField(source='status.id')
    status = serializers.CharField(source='status.name')
    css_style = serializers.CharField(source='status.css_style')
    schema_id = serializers.IntegerField(source='schema.id')

    class Meta:
        model = DataSets
        fields = ('id', 'filepath', 'count_rows', 'created', 'status_id', 'status', 'css_style', 'schema_id')
