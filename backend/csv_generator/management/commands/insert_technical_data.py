from django.core.management.base import BaseCommand
from django.conf import settings

from csv_generator.models import ColumnType, StringCharacter, ColumnSeparator, StatusDataSet


class Command(BaseCommand):
    help = 'Create default data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Start create Field types.')
        ColumnType.objects.create(id=1, name='Full name')
        ColumnType.objects.create(id=2, name='Job')
        ColumnType.objects.create(id=3, name='Email')
        ColumnType.objects.create(id=4, name='Domain name')
        ColumnType.objects.create(id=5, name='Phone number')
        ColumnType.objects.create(id=6, name='Company name')
        ColumnType.objects.create(id=7, name='Text')
        ColumnType.objects.create(id=8, name='Integer')
        ColumnType.objects.create(id=9, name='Address')
        ColumnType.objects.create(id=10, name='Date')
        self.stdout.write('Field types has been created')
        self.stdout.write('Start create String characters.')
        StringCharacter.objects.create(id=1, name='Single quote (\')', symbol='\'')
        StringCharacter.objects.create(id=2, name='Double quote (\")', symbol='\"')
        self.stdout.write('String characters has been created')
        self.stdout.write('Start create Column separators.')
        ColumnSeparator.objects.create(id=1, name='Comma (,)', symbol=',')
        ColumnSeparator.objects.create(id=2, name='Semicolon (;)', symbol=';')
        self.stdout.write('Column separators has been created')
        self.stdout.write('Start create Column separators.')
        StatusDataSet.objects.create(id=1, name='Failed', css_style='bg-danger')
        StatusDataSet.objects.create(id=2, name='In progress', css_style='bg-warning')
        StatusDataSet.objects.create(id=3, name='Success', css_style='bg-success')

        self.stdout.write('Column separators has been created')
