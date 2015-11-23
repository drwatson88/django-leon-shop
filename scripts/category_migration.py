# coding: utf-8


import sys
import os


project_dir = u'/'.join(os.getcwd().split(u'/')[:-2])
sys.path.append(project_dir)
sys.path.append(os.path.join(project_dir, u'apps'))
os.environ[u'DJANGO_SETTINGS_MODULE'] = u'settings'

import django
django.setup()


from catalog.models import  CategoryXML, Tovar, SubTovar, TovarAttachment, Group, Pack, \
                            Status, PrintType, Stock, Maker, Category