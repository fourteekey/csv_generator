from django.db import models
from django.contrib.auth import get_user_model


class ColumnSeparator(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=1)

    class Meta:
        db_table = 'column_separator'

    def __str__(self):
        return self.name


class StringCharacter(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=1)

    class Meta:
        db_table = 'string_character'

    def __str__(self):
        return self.name


class ColumnType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'column_type'

    def __str__(self):
        return self.name


class StatusDataSet(models.Model):
    name = models.CharField(max_length=100)
    css_style = models.CharField(max_length=50)

    class Meta:
        db_table = 'status_data_set'

    def __str__(self):
        return self.name


class Schemas(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    column_separator = models.ForeignKey('ColumnSeparator', on_delete=models.DO_NOTHING)
    string_character = models.ForeignKey('StringCharacter', on_delete=models.DO_NOTHING)

    modified = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_schemas'

    def __str__(self):
        return self.filename


class SchemaColumns(models.Model):
    schema = models.ForeignKey('Schemas', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    integer_from = models.IntegerField(default=None, null=True)
    integer_to = models.IntegerField(default=None, null=True)
    column_type = models.ForeignKey('ColumnType', on_delete=models.DO_NOTHING)

    is_deleted = models.SmallIntegerField(default=None, null=True)

    class Meta:
        db_table = 'schema_columns'
        ordering = ('order',)


class DataSets(models.Model):
    schema = models.ForeignKey('Schemas', on_delete=models.CASCADE)
    filepath = models.CharField(max_length=200)
    task_id = models.CharField(max_length=100, default=None, null=True)
    count_rows = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_created=True)
    status = models.ForeignKey('StatusDataSet', on_delete=models.DO_NOTHING, default=2)

    class Meta:
        db_table = 'schema_datasets'
        ordering = ('-id',)
