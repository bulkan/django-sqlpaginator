from setuptools import setup

from version import __version__

setup(
    name='django-sqlpaginator',
    packages=['sqlpaginator'],
    version=__version__,
    description='django app that does pagination on using raw sql on a Model',
    author='Bulkan Evcimen',
    author_email='bulkan@gmail.com',
    url='https://github.com/bulkan/django-sqlpaginator',
    #install_requires=[
        #'django'
    #],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
