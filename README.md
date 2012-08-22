django-sqlpaginator
===================

Paginate raw sql queries using LIMIT and OFFSET

It will also supports ORDER BY queries

installation
============

To install for the moment use the following

    pip install git+git://github.com/bulkan/django-sqlpaginator.git

In settings.py

    INSTALLED_APPS = (
        ...
        'sqlpaginator',
        ...
    )

Thats it !!

usage
=====

Pretty much same as django.core.pagination.Paginator

If you have the following models

    class Album(models.Model):
         albumid = models.IntegerField(primary_key=True, db_column=u'AlbumId')
         title = models.TextField(db_column=u'Title') # Field name made lowercase. This field type is a guess.
         artistid = models.IntegerField(db_column=u'ArtistId')

    class Artist(models.Model):
         artistid = models.IntegerField(primary_key=True, db_column=u'ArtistId')
         name = models.TextField(db_column=u'Name', blank=True) # Field name made lowercase. This field type is a guess.


and you want to paginate on Albums, then inside a view;


    from sqlpaginator.paginator import SqlPaginator
    from models import Album

    def get_albums(request, page=1):
        sql = "select * from FROM %s" % Album._meta.db_table
        paginator = SqlPaginator(sql, Album, page=page)

        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            albums = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            albums = paginator.page(sp.num_pages)

        return render_to_response('albums_list.html', {'albums': albums})


 In the template ```albums_list.html```


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


contributing
=====

* Clone repo
* Change code
* Add tests
* Run the tests

    nosetests -s --with-coverage --cover-package=sqlpaginator
* Submit pull request
