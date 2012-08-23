from unittest import TestCase

from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger

from models import Artist, Album
from sqlpaginator.paginator import SqlPaginator


class SqlPaginatorTests(TestCase):
    album_sql = "select albumid from %s" % Album._meta.db_table
    artist_sql = "select * from %s" % Artist._meta.db_table

    def test_data_in_db(self):
        ''' test to see if the models that were created for the Chinook
        db using the inspectdb management command actually return data '''

        self.assertTrue(Artist.objects.all().count() > 0)

    def test_sql_query(self):
        ''' test sql query created has the appropriate pagination clauses '''

        sql = "SELECT DISTINCT(auth_user.id) FROM auth_user WHERE (DATE_PART('YEAR',AGE(auth_user.dob)) > 10)"
        sql_paginator = SqlPaginator(sql, User)
        self.assertTrue('limit' in sql_paginator.sql)
        self.assertTrue('order' in sql_paginator.sql)

    def test_returns_objects(self):
        sql_paginator = SqlPaginator(self.artist_sql, Artist,
                                     page=1, order_by='artistid')
        artists = sql_paginator.page(1)
        self.assertTrue(len(artists) > 0)

    def test_has_functions(self):
        paginator = SqlPaginator(self.artist_sql, Artist, page=6,
                                 order_by='name', per_page=3)
        artists = paginator.page(6)
        self.assertTrue(len(artists) > 0)
        self.assertTrue(artists.has_next())
        self.assertTrue(artists.has_previous())

    def test_order_by(self):
        paginator = SqlPaginator(self.artist_sql, Artist,
                                 page=6, order_by='artistid')
        artists = paginator.page(6)
        self.assertEqual([a.artistid for a in artists.object_list][0], 51)

    def test_albums(self):
        page = 1
        paginator = SqlPaginator(self.album_sql, Album,
                                 page=page, order_by='title')

        albums = paginator.page(page)
        self.assertTrue(len(albums) > 0)

        # last page
        albums = paginator.page(paginator.num_pages)
        self.assertTrue(len(albums) > 0)

    def test_order_by_direction(self):
        page = 1
        paginator = SqlPaginator(self.album_sql, Album,
                                 page=page, order_by='albumid')

        albums = [a.albumid for a in paginator.page(page)]
        self.assertTrue(len(albums) > 0)
        self.assertEqual(albums, range(1, 11))

        paginator = SqlPaginator(self.album_sql, Album, page=page,
                                 order_by='albumid', direction='desc')

        albums = [a.albumid for a in paginator.page(page)]
        self.assertEqual(albums, list(reversed(range(338, 348))))

    def test_invalid_order_by_column(self):
        page = 1
        self.assertRaises(ValueError, SqlPaginator, self.album_sql, Album,
                                 page=page, order_by='albumid$$$')

    def test_zero_count(self):
        ''' what happens when the sql creates 0 rows (count=0) '''

        sql = "%s WHERE albumid < 0" % self.album_sql
        paginator = SqlPaginator(sql, Album, page=1,
                                 order_by='albumid', direction='desc')

        self.assertEqual(len([a.albumid for a in paginator.page(1)]), 0)

    def test_invalid_number(self):
        self.assertRaises(ValueError, SqlPaginator, self.album_sql, Album,
                                 page="one", order_by='albumid')

        paginator = SqlPaginator(self.album_sql, Album, page=1,
                                 order_by='albumid', direction='descending')

        self.assertRaises(PageNotAnInteger, paginator.page, 'one')
        self.assertRaises(EmptyPage, paginator.page, paginator.num_pages + 1)
        self.assertRaises(EmptyPage, paginator.page, -1)
