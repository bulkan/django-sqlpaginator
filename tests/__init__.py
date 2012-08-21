import sys

# add the dir one level up to PYTHONPATH so we can import stuff for testing
sys.path.append('../')

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from django.test.utils import setup_test_environment
setup_test_environment()
