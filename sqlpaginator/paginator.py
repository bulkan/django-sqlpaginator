import logging

from math import ceil

from django.db import connection
from django.core.paginator import Page, Paginator


logger = logging.getLogger(__name__)


class SqlPaginator(Paginator):
    ''' inherits from django.core.paginator to provide same API '''

    def __init__(self, initial_sql, model, order_by='id', page=1, per_page=10):

        self.per_page = per_page

        self.model = model

        self.orphans = 0

        self._num_pages = self._count = None

        self.initial_sql = initial_sql

        self.object_list = []

        self.page_num = page
        print 'page: %d' % page

        # dict to resolve the sql template with
        self.d = {'sql': initial_sql,
             'order_by': order_by,
             'offset': int(page - 1) * self.per_page,
             'limit': self.per_page
             }

        self._tsql = '%(sql)s ORDER BY %(order_by)s LIMIT %(limit)d OFFSET %(offset)d' 
        self._sql = self._tsql % self.d

    def get_sql(self):
        return self._sql

    sql = property(get_sql)

    def _get_count(self):
        if self._count is None:
            cursor = connection.cursor()
            sql = 'SELECT COUNT(au.id) FROM %(table_name)s as au' % {'table_name': self.model._meta.db_table}
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

    def page(self, number):
        number = self.validate_number(number)

        cursor = connection.cursor()

        self.d.update({'offset': (number - 1) * 10})

        #print '*' * 80
        #print 'count: %d' % self.count
        #print 'num_pages: %d' % self.num_pages

        sql = self._tsql % self.d
        logger.info("sql: %s" % sql)
        #print sql

        cursor.execute(sql)
        rows = cursor.fetchall()
        ids = [row[0] for row in rows]

        self.object_list = self.model.objects.filter(id__in=ids)

        #print object_list

        #print '*' * 80

        #return Page(object_list[bottom:top], number, self)
        return Page(self.object_list, number, self)
