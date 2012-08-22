from unittest import TestCase

from django.contrib.auth.models import User


from models import Artist
from sqlpaginator.paginator import SqlPaginator


class SqlPaginatorTests(TestCase):
    def test_data_in_db(self):
        ''' test to see if the models that were created for the Chinook
        db using the inspectdb management command actually return data '''

        self.assertTrue(Artist.objects.all().count() > 0)

    def test_sql_query(self):
        ''' test that sql query created has the appropriate pagination clauses '''

        sql = "SELECT DISTINCT(auth_user.id) FROM auth_user WHERE (DATE_PART('YEAR',AGE(auth_user.dob)) > 10)"
        sql_paginator = SqlPaginator(sql, User)
        self.assertTrue('LIMIT' in sql_paginator.sql)
        self.assertTrue('ORDER' in sql_paginator.sql)

    def test_returns_objects(self):
        sql = "select distinct(artistid) from %s" % Artist._meta.db_table
        sql_paginator = SqlPaginator(sql, Artist, page=1, order_by='artistid')
        artists = sql_paginator.page(1)
        self.assertTrue(len(artists) > 0)

    def test_has_functions(self):
        sql = "select artistid from %s" % Artist._meta.db_table
        sql_paginator = SqlPaginator(sql, Artist, page=6, order_by='name')
        artists = sql_paginator.page(6)
        self.assertTrue(len(artists) > 0)
        self.assertTrue(artists.has_next())
        self.assertTrue(artists.has_previous())

    def test_order_by(self):
        sql = "select artistid from %s" % Artist._meta.db_table
        sql_paginator = SqlPaginator(sql, Artist, page=6, order_by='artistid')
        artists = sql_paginator.page(6)
        self.assertEqual([a.artistid for a in artists.object_list][0], 51)
