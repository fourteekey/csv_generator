from __future__ import absolute_import
import pymysql

from .celery import app as celery_app

__all__ = ('celery_app',)

pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()

