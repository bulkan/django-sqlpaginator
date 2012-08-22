from unittest import TestCase

from django.contrib.auth.models import User


from models import Artist, Album
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
        self.assertTrue('limit' in sql_paginator.sql)
        self.assertTrue('order' in sql_paginator.sql)

    def test_returns_objects(self):
        sql = "select distinct(artistid) from %s" % Artist._meta.db_table
        sql_paginator = SqlPaginator(sql, Artist, page=1, order_by='artistid')
        artists = sql_paginator.page(1)
        self.assertTrue(len(artists) > 0)

    def test_has_functions(self):
        sql = "select * from %s" % Artist._meta.db_table
        sql_paginator = SqlPaginator(sql, Artist, page=6, order_by='name', per_page=3)
        artists = sql_paginator.page(6)
        self.assertTrue(len(artists) > 0)
        self.assertTrue(artists.has_next())
        self.assertTrue(artists.has_previous())

    def test_order_by(self):
        sql = "select * from %s" % Artist._meta.db_table
        sql_paginator = SqlPaginator(sql, Artist, page=6, order_by='artistid')
        artists = sql_paginator.page(6)
        self.assertEqual([a.artistid for a in artists.object_list][0], 51)

    def test_albums(self):
        sql = "select * from %s" % Album._meta.db_table
        page = 1
        paginator = SqlPaginator(sql, Album, page=page, order_by='title')
        albums = paginator.page(page)
        self.assertTrue(len(albums) > 0)

        # last page
        albums = paginator.page(paginator.num_pages)
        self.assertTrue(len(albums) > 0)

    def test_order_by_direction(self):
        sql = "select * from %s" % Album._meta.db_table
        page = 1
        paginator = SqlPaginator(sql, Album, page=page, order_by='albumid')
        albums = [a.albumid for a in paginator.page(page)]
        self.assertTrue(len(albums) > 0)
        self.assertEqual(albums, range(1, 11))

        paginator = SqlPaginator(sql, Album, page=page, order_by='albumid', direction='desc')
        albums = [a.albumid for a in paginator.page(page)]
        self.assertEqual(albums, list(reversed(range(338, 348))))
