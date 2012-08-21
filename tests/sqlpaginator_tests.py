from unittest import TestCase

from django.contrib.auth.models import User


from models import Artist
from sqlpaginator.paginator import SqlPaginator


class SqlPaginatorTests(TestCase):

    def test_basic(self):
        sql = "SELECT DISTINCT(auth_user.id) FROM auth_user WHERE (DATE_PART('YEAR',AGE(auth_user.dob)) > 10)"
        sql_paginator = SqlPaginator(User, sql)
        self.assertTrue('LIMIT' in sql_paginator.sql)

    def test_pagination(self):
        sql = "select distinct(artistid) from artist"
        sql_paginator = SqlPaginator(sql, Artist, page=1, order_by='artistid')
        artists = sql_paginator.page(1)
        self.assertTrue(len(artists) > 0)
