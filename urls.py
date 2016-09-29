"""

"""
import logging

from django.conf.urls.defaults import *

# This new app handles the request to the URL by responding with the view which is loaded 
# from portal.plugins.synonyms.views.py. Inside that file is a class which responsedxs to the 
# request, and sends in the arguments template - the html file to view.
# name is shortcut name for the urls.

urlpatterns = patterns('portal.plugins.synonyms.views',
    url(r'^$', 'SynonymsView', kwargs={'template': 'synonyms/synonyms_list.html'}, name='synonyms_list'),
    url(r'^synonym/add$', 'SynonymEditView', kwargs={'template': 'synonyms/synonym_edit.html'}, name='synonym_new'),
    url(r'^synonym/(?P<synonym_id>\d+)$', 'SynonymEditView', kwargs={'template': 'synonyms/synonym_edit.html'}, name='synonym_edit'),
    url(r'^synonym/(?P<synonym_id>\d+)/remove$', 'SynonymRemoveView', kwargs={}, name='synonym_remove'),
    url(r'^synonym/(?P<parent_id>\d+)/(?P<synonym_id>\d+)$', 'SynonymEditView', kwargs={'template': 'synonyms/synonym_edit.html'}, name='synonym_editchild'),
    url(r'^synonym/(?P<parent_id>\d+)/add$', 'SynonymEditView', kwargs={'template': 'synonyms/synonym_edit.html'}, name='synonym_addchild'),
)
