from math import ceil

from django.db import connection
from django.core.paginator import Page


class Paginator(object):
    pass


class SqlPaginator(Paginator):
    def __init__(self, initial_sql, model, order_by='id', page=1, per_page=10):

        self.per_page = per_page

        self.orphans = 0

        self._num_pages = self._count = None

        self.initial_sql = initial_sql

        self.d = {'sql': initial_sql,
             'order_by': order_by,
             'offset': int(page - 1) * 10,
             'limit': 10
             }

        self._sql = '%(sql)s ORDER BY %(order_by)s OFFSET %(offset)d LIMIT %(limit)d' % self.d

    def get_sql(self):
        return self._sql

    sql = property(get_sql)

    def _get_count(self):
        if self._count is None:
            cursor = connection.cursor()
            sql = 'SELECT COUNT(au.id) FROM (%s) as au' % self.sql
            cursor.execute(sql)
            rows = cursor.fetchall()

            self._count = int(rows[0][0])
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

    def page(self, number):
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page

        if top + self.orphans >= self.count:
            top = self.count

        cursor = connection.cursor()
        self.d.update({'offset': number})

        cursor.execute(self._sql)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]

        members = self.model.objects.filter(id__in=ids)

        return Page(members[bottom:top], number, self)
