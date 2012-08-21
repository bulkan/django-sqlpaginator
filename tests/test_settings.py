import os

FOLDER_ROOT = os.path.normpath(os.path.dirname(__file__))
print FOLDER_ROOT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(FOLDER_ROOT, 'chinook/Chinook_Sqlite.sqlite')
    }
}
