# This is an auto-generated Django model module.

from django.db import models

class Album(models.Model):
    albumid = models.IntegerField(primary_key=True, db_column=u'AlbumId')
    title = models.TextField(db_column=u'Title') # Field name made lowercase. This field type is a guess.
    artistid = models.IntegerField(db_column=u'ArtistId')
    class Meta:
        db_table = u'Album'

    def __unicode__(self):
        return "<Album: %s, %d>" % (self.title, self.artistid)

class Artist(models.Model):
    artistid = models.IntegerField(primary_key=True, db_column=u'ArtistId')
    name = models.TextField(db_column=u'Name', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Artist'

class Customer(models.Model):
    customerid = models.IntegerField(primary_key=True, db_column=u'CustomerId')
    firstname = models.TextField(db_column=u'FirstName') # Field name made lowercase. This field type is a guess.
    lastname = models.TextField(db_column=u'LastName') # Field name made lowercase. This field type is a guess.
    company = models.TextField(db_column=u'Company', blank=True) # Field name made lowercase. This field type is a guess.
    address = models.TextField(db_column=u'Address', blank=True) # Field name made lowercase. This field type is a guess.
    city = models.TextField(db_column=u'City', blank=True) # Field name made lowercase. This field type is a guess.
    state = models.TextField(db_column=u'State', blank=True) # Field name made lowercase. This field type is a guess.
    country = models.TextField(db_column=u'Country', blank=True) # Field name made lowercase. This field type is a guess.
    postalcode = models.TextField(db_column=u'PostalCode', blank=True) # Field name made lowercase. This field type is a guess.
    phone = models.TextField(db_column=u'Phone', blank=True) # Field name made lowercase. This field type is a guess.
    fax = models.TextField(db_column=u'Fax', blank=True) # Field name made lowercase. This field type is a guess.
    email = models.TextField(db_column=u'Email') # Field name made lowercase. This field type is a guess.
    supportrepid = models.IntegerField(null=True, db_column=u'SupportRepId', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Customer'

class Employee(models.Model):
    employeeid = models.IntegerField(primary_key=True, db_column=u'EmployeeId') # Field name made lowercase.
    lastname = models.TextField(db_column=u'LastName') # Field name made lowercase. This field type is a guess.
    firstname = models.TextField(db_column=u'FirstName') # Field name made lowercase. This field type is a guess.
    title = models.TextField(db_column=u'Title', blank=True) # Field name made lowercase. This field type is a guess.
    reportsto = models.IntegerField(null=True, db_column=u'ReportsTo', blank=True) # Field name made lowercase.
    birthdate = models.DateTimeField(null=True, db_column=u'BirthDate', blank=True) # Field name made lowercase.
    hiredate = models.DateTimeField(null=True, db_column=u'HireDate', blank=True) # Field name made lowercase.
    address = models.TextField(db_column=u'Address', blank=True) # Field name made lowercase. This field type is a guess.
    city = models.TextField(db_column=u'City', blank=True) # Field name made lowercase. This field type is a guess.
    state = models.TextField(db_column=u'State', blank=True) # Field name made lowercase. This field type is a guess.
    country = models.TextField(db_column=u'Country', blank=True) # Field name made lowercase. This field type is a guess.
    postalcode = models.TextField(db_column=u'PostalCode', blank=True) # Field name made lowercase. This field type is a guess.
    phone = models.TextField(db_column=u'Phone', blank=True) # Field name made lowercase. This field type is a guess.
    fax = models.TextField(db_column=u'Fax', blank=True) # Field name made lowercase. This field type is a guess.
    email = models.TextField(db_column=u'Email', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Employee'

class Genre(models.Model):
    genreid = models.IntegerField(primary_key=True, db_column=u'GenreId') # Field name made lowercase.
    name = models.TextField(db_column=u'Name', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Genre'

class Invoice(models.Model):
    invoiceid = models.IntegerField(primary_key=True, db_column=u'InvoiceId') # Field name made lowercase.
    customerid = models.IntegerField(db_column=u'CustomerId') # Field name made lowercase.
    invoicedate = models.DateTimeField(db_column=u'InvoiceDate') # Field name made lowercase.
    billingaddress = models.TextField(db_column=u'BillingAddress', blank=True) # Field name made lowercase. This field type is a guess.
    billingcity = models.TextField(db_column=u'BillingCity', blank=True) # Field name made lowercase. This field type is a guess.
    billingstate = models.TextField(db_column=u'BillingState', blank=True) # Field name made lowercase. This field type is a guess.
    billingcountry = models.TextField(db_column=u'BillingCountry', blank=True) # Field name made lowercase. This field type is a guess.
    billingpostalcode = models.TextField(db_column=u'BillingPostalCode', blank=True) # Field name made lowercase. This field type is a guess.
    total = models.TextField(db_column=u'Total') # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Invoice'

class Invoiceline(models.Model):
    invoicelineid = models.IntegerField(primary_key=True, db_column=u'InvoiceLineId') # Field name made lowercase.
    invoiceid = models.IntegerField(db_column=u'InvoiceId') # Field name made lowercase.
    trackid = models.IntegerField(db_column=u'TrackId') # Field name made lowercase.
    unitprice = models.TextField(db_column=u'UnitPrice') # Field name made lowercase. This field type is a guess.
    quantity = models.IntegerField(db_column=u'Quantity') # Field name made lowercase.
    class Meta:
        db_table = u'InvoiceLine'

class Mediatype(models.Model):
    mediatypeid = models.IntegerField(primary_key=True, db_column=u'MediaTypeId') # Field name made lowercase.
    name = models.TextField(db_column=u'Name', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'MediaType'

class Playlist(models.Model):
    playlistid = models.IntegerField(primary_key=True, db_column=u'PlaylistId') # Field name made lowercase.
    name = models.TextField(db_column=u'Name', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Playlist'

class Playlisttrack(models.Model):
    playlistid = models.IntegerField(primary_key=True, db_column=u'PlaylistId') # Field name made lowercase.
    trackid = models.IntegerField(primary_key=True, db_column=u'TrackId') # Field name made lowercase.
    class Meta:
        db_table = u'PlaylistTrack'

class Track(models.Model):
    trackid = models.IntegerField(primary_key=True, db_column=u'TrackId') # Field name made lowercase.
    name = models.TextField(db_column=u'Name') # Field name made lowercase. This field type is a guess.
    albumid = models.IntegerField(null=True, db_column=u'AlbumId', blank=True) # Field name made lowercase.
    mediatypeid = models.IntegerField(db_column=u'MediaTypeId') # Field name made lowercase.
    genreid = models.IntegerField(null=True, db_column=u'GenreId', blank=True) # Field name made lowercase.
    composer = models.TextField(db_column=u'Composer', blank=True) # Field name made lowercase. This field type is a guess.
    milliseconds = models.IntegerField(db_column=u'Milliseconds') # Field name made lowercase.
    bytes = models.IntegerField(null=True, db_column=u'Bytes', blank=True) # Field name made lowercase.
    unitprice = models.TextField(db_column=u'UnitPrice') # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Track'

