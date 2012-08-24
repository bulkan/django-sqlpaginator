from setuptools import setup

__version__ = ''
execfile('sqlpaginator/version.py')

description = '''django app that does pagination and ordering using raw
sql on a Model. It has the same API as the django.core.pagination.Paginator'''

setup(
    name='django-sqlpaginator',
    packages=['sqlpaginator'],
    version=__version__,
    description=description,
    author='Bulkan Evcimen',
    author_email='bulkan@gmail.com',
    url='https://github.com/bulkan/django-sqlpaginator',
    #dependency_links=["https://github.com/andialbrecht/sqlparse/tarball/master"],
    install_requires=[
        #'distribute',
        'sqlparse'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
