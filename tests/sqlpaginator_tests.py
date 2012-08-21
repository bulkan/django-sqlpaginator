from unittest import TestCase

from django.contrib.auth.models import User


from django.db import connection
from sqlpaginator.paginator import SqlPaginator


class SqlPaginatorTests(TestCase):

    def test_basic(self):
        sql = "SELECT DISTINCT(auth_user.id) FROM auth_user WHERE (DATE_PART('YEAR',AGE(auth_user.dob)) > 10)"
        sql_paginator = SqlPaginator(User, sql)
        self.assertTrue('LIMIT' in sql_paginator.sql)

