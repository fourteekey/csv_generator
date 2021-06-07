import csv
import logging
import dropbox

from django.conf import settings
from faker import Faker
from celery import shared_task
from celery.utils.log import get_task_logger

from .models import *


logger = get_task_logger(__name__)
fake = Faker()


@shared_task(name="generate_data_set")
def generate_dataset_task(dataset_id):
    dataset = DataSets.objects.get(id=dataset_id)
    columns = SchemaColumns.objects.filter(schema=dataset.schema)
    column_names = [column.name for column in columns]

    filepath = settings.MEDIA_ROOT + dataset.filepath

    # Base info
    SLICE_ROW = 1000  # Write row by small part.
    count_row = dataset.count_rows

    #  Create file
    with open(filepath, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=column_names,
                                delimiter=dataset.schema.column_separator.symbol,
                                quotechar=dataset.schema.string_character.symbol,
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()

    #  Insert rows
    while count_row > 0:
        rows = []
        if count_row - SLICE_ROW < 0: SLICE_ROW = count_row
        for i in range(1, SLICE_ROW + 1):
            row = {}
            for column in columns:
                if column.column_type.id == 1:
                    row.update({column.name: fake.name()})
                elif column.column_type.id == 2:
                    row.update({column.name: fake.job()})
                elif column.column_type.id == 3:
                    row.update({column.name: fake.email()})
                elif column.column_type.id == 4:
                    row.update({column.name: fake.domain_name()})
                elif column.column_type.id == 5:
                    row.update({column.name: fake.phone_number()})
                elif column.column_type.id == 6:
                    row.update({column.name: fake.company()})
                elif column.column_type.id == 7:
                    row.update({column.name: fake.text()})
                elif column.column_type.id == 8:
                    row.update({column.name: fake.random_int(min=column.integer_from, max=column.integer_to)})
                elif column.column_type.id == 9:
                    row.update({column.name: fake.address()})
                elif column.column_type.id == 10:
                    row.update({column.name: fake.date()})
            rows.append(row)
        with open(filepath, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=column_names,
                                    delimiter=dataset.schema.column_separator.symbol,
                                    quotechar=dataset.schema.string_character.symbol,
                                    quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(rows)
        count_row -= SLICE_ROW

    file_url = None
    dbx = dropbox.Dropbox(settings.DROPBOX_API)
    with open(filepath, 'rb') as f:
        dbx.files_upload(f.read(), filepath)
        try:
            dbx.sharing_create_shared_link_with_settings(filepath)
        except Exception:
            pass
        links = dbx.sharing_list_shared_links(filepath).links
        if links: file_url = links[0].url

    dataset.file_url = file_url
    dataset.status = StatusDataSet.objects.get(id=3)
    dataset.save()
    return


@shared_task
def clean_task():
    from django.db import connection
    cursor = connection.cursor()
    try:
        cursor.execute('UPDATE `schema_datasets` SET `status_id`=1 '
                       'WHERE `status_id`=2 AND TIMESTAMPDIFF(MINUTE,`updated`, NOW()) > 15')
        connection.commit()
    except Exception as e:
        logging.error('CrontabError: ', e)
