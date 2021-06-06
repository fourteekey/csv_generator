from datetime import datetime

from .models import *
from .serializers import *
from .tasks import *


def get_column_separator():
    return ColumnSeparatorSerializer(ColumnSeparator.objects.all(), many=True).data


def get_column_type():
    return ColumnTypeSerializer(ColumnType.objects.all(), many=True).data


def get_string_character():
    return StringCharacterSerializer(StringCharacter.objects.all(), many=True).data


def get_user_schemas(user):
    schema = Schemas.objects.filter(user=user, is_deleted=False)
    return SchemaSerializer(schema, many=True).data


def get_user_schema_by_idQuerySet(user, schema_id):
    schema = Schemas.objects.filter(user=user, id=schema_id, is_deleted=False)
    if not schema: return
    return schema[0]


def get_user_detail_schema_by_id(user, schema_id):
    schema = Schemas.objects.filter(user=user, id=schema_id, is_deleted=False)
    if not schema: return
    return SchemaDetailSerializer(schema[0]).data


def get_datasets(user, schema_id):
    datasets = DataSets.objects.filter(schema__user=user, schema__id=schema_id)
    return DataSetSerializer(datasets, many=True).data


def get_dataset_by_idQuerySet(user, dataset_id):
    dataset = DataSets.objects.filter(schema__user=user, id=dataset_id)
    if not dataset: return
    return dataset[0]


def create_schema(user, filename, column_separator_id, string_character_id):
    column_separator = ColumnSeparator.objects.filter(id=column_separator_id)
    string_character = StringCharacter.objects.filter(id=string_character_id)
    if not column_separator or not string_character: return
    schema = Schemas.objects.create(user=user,
                                    filename=filename,
                                    column_separator=column_separator[0],
                                    string_character=string_character[0])
    return schema


def add_columns_to_schema(schema, columns):
    for column in columns:
        order = column.get('Order', None)
        name = column.get('ColumnName', None)
        column_type_id = column.get('ColumnType', None)
        integer_from = column.get('MinInteger', None) or None
        integer_to = column.get('MaxInteger', None) or None

        if not name or not order or not column_type_id: return ''

        column_type = ColumnType.objects.filter(id=column_type_id)
        if not column_type: return 'Invalid ColumnType'

        SchemaColumns.objects.create(schema=schema, name=name, order=order,
                                     integer_from=integer_from, integer_to=integer_to, column_type=column_type[0])


def delete_schema(schema):
    schema.delete()


def deactivate_schema(schema):
    schema.is_deleted = True
    schema.save()


def delete_schema_columns(schema):
    SchemaColumns.objects.filter(schema=schema).delete()


def update_schema(schema, filename, column_separator_id, string_character_id):
    if filename and schema.filename != filename:
        schema.filename = filename
    if column_separator_id and schema.column_separator.id != column_separator_id:
        column_separator = ColumnSeparator.objects.filter(id=column_separator_id)
        if not column_separator: return 'Invalid column separator'
        schema.column_separator = column_separator[0]
    if string_character_id and schema.string_character.id != string_character_id:
        string_character = StringCharacter.objects.filter(id=column_separator_id)
        if not string_character: return 'Invalid string character'
        schema.string_character = string_character[0]
    schema.save()


def generate_dataset_csv(schema, count_rows):
    date_str = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    filepath = f'/{schema.user.id}_{schema.filename}_{date_str}.csv'

    dataset = DataSets.objects.create(schema=schema,
                                      filepath=filepath,
                                      count_rows=count_rows,
                                      created=datetime.now().date())
    task = generate_dataset_task.delay(dataset_id=dataset.id)
    dataset.task_id = task.id
    dataset.save()
    return DataSetSerializer(dataset).data
