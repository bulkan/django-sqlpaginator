import logging

from math import ceil

from django.db import connection
from django.core.paginator import Page

from django.core.paginator import EmptyPage, PageNotAnInteger


logger = logging.getLogger(__name__)


class SqlPaginator(object):

    def __init__(self, initial_sql, model, order_by='id', page=1,
                count=None, per_page=10, direction='asc'):

        # if these are not an int then fail
        self.page_num = int(page)
        self.per_page = int(per_page)
        try:
            self._count = int(count)
        except TypeError:
            self._count = None

        # need the model class to do some sql validation
        self.model = model

        self._num_pages = None
        self.orphans = 0
        self.initial_sql = initial_sql
        self.object_list = []

        self.allow_empty_first_page = True

        # resolve the model fields into their names
        self._model_fields = [f.name for f in model._meta.fields]

        self._db_table = self.model._meta.db_table

        # validate sql fields
        if order_by not in self._model_fields:
            raise ValueError("%s does is not a valid column in %s" % (order_by, self._db_table))

        self.order_by = order_by

        self.direction = direction
        if direction.lower() not in ['asc', 'desc']:
            self.direction = 'asc'

        # dict to resolve the sql template with
        self.d = {'sql': initial_sql,
                  'order_by': order_by,
                  'offset': int(page - 1) * self.per_page,
                  'limit': self.per_page,
                  'direction': direction,
                 }

        self._tsql = '%(sql)s order by %(order_by)s %(direction)s limit %(limit)d offset %(offset)d'
        self._sql = self._tsql % self.d

    def get_sql(self):
        return self._sql
    sql = property(get_sql)

    def _get_count(self):
        if self._count is None:
            cursor = connection.cursor()
            sql = "select count(distinct(%s)) from (%s) as q" % (self.model._meta.pk.name, self.initial_sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            count = int(rows[0][0])
            self._count = count
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        if self._num_pages is None:
            if self.count == 0:
                self._num_pages = 0
            else:
                hits = max(1, self.count, self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))

        return self._num_pages
    num_pages = property(_get_num_pages)

    def validate_number(self, number):
        "Validates the given 1-based page number."
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number, order_by=None, direction=None):
        number = self.validate_number(number)

        if not order_by and order_by not in self._model_fields:
            order_by = self.order_by

        if not direction or direction.lower() not in ['asc', 'desc']:
            direction = self.direction

        self.d.update({'offset': (number - 1) * self.per_page,
                       'order_by': order_by,
                       'direction': direction})

        logger.debug('count: %d' % self.count)
        logger.debug('num_pages: %d' % self.num_pages)

        sql = self._tsql % self.d
        logger.debug("sql: %s" % sql)

        self.object_list = list(self.model.objects.raw(sql))

        return Page(self.object_list, number, self)
