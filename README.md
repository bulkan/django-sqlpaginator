[![Build Status](https://secure.travis-ci.org/bulkan/django-sqlpaginator.png?branch=master)](http://travis-ci.org/bulkan/django-sqlpaginator)
[![PyPi downloads](https://pypip.in/d/django-sqlpaginator/badge.png)](https://crate.io/packages/django-sqlpaginator/)


django-sqlpaginator
===================

Paginate raw sql queries using LIMIT and OFFSET

It will also supports ORDER BY queries

installation
============

To install from pypi
    
    pip install django-sqlpaginator

To get the latest (and possibly non stable version) from git

    pip install git+git://github.com/bulkan/django-sqlpaginator.git

You also need to install sqlparser

    pip install git+git://github.com/andialbrecht/sqlparse.git

In settings.py

```python
    INSTALLED_APPS = (
        ...
        'sqlpaginator',
        ...
    )
```

Thats it !!

usage
=====

Pretty much same as django.core.pagination.Paginator

If you have the following models

```python
    class Album(models.Model):
         albumid = models.IntegerField(primary_key=True, db_column=u'AlbumId')
         title = models.TextField(db_column=u'Title') 
         artistid = models.IntegerField(db_column=u'ArtistId')

    class Artist(models.Model):
         artistid = models.IntegerField(primary_key=True, db_column=u'ArtistId')
         name = models.TextField(db_column=u'Name', blank=True) 
```


and you want to paginate on Albums, then inside a view;

```python

    from sqlpaginator.paginator import SqlPaginator
    from models import Album

    def get_albums(request, page=1):
        sql = "select * from %s" % Album._meta.db_table
        paginator = SqlPaginator(sql, Album, page=page, order_by='title')

        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            albums = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            albums = paginator.page(paginator.num_pages)

        return render_to_response('albums_list.html', {'albums': albums})
```

 In the template ```albums_list.html```

```python
    {% for album in albums %}
        {# Each "album" is a Album model object. #}
        {{ album.title|upper }}<br />
    {% endfor %}

    <div class="pagination">
        <span class="step-links">
            {% if albums.has_previous %}
                <a href="?page={{ albums.previous_page_number }}">previous</a>
            {% endif %}

            <span class="current">
                Page {{ albums.number }} of {{ albums.paginator.num_pages }}.
            </span>

            {% if albums.has_next %}
                <a href="?page={{ albums.next_page_number }}">next</a>
            {% endif %}
        </span>
    </div>
```

contributing
=====

* Clone repo
* Change code
* Add tests
* Run the tests
```nosetests -s --with-coverage --cover-package=sqlpaginator```
* Submit pull request
