"""
This is where you can write a lot of the code that responds to URLS - such as a page request from a browser
or a HTTP request from another application.

From here you can follow the Cantemo Portal Developers documentation for specific code, or for generic 
framework code refer to the Django developers documentation. 

"""
import logging

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from portal.generic.baseviews import ClassView
from portal.vidispine.iitem import ItemHelper
from portal.vidispine.iexception import NotFoundError

from portal.plugins.synonyms.models import Synonym
from portal.plugins.synonyms.forms import SynonymForm
from portal.plugins.synonyms.models import TagField
from portal.plugins.synonyms.forms import TagFieldForm


log = logging.getLogger(__name__)


class SynonymsView(ClassView):

    def __call__(self):
        
        # Get all Metadata Mappings
        synonyms = Synonym.objects.filter(parent__isnull=True)
        
        ctx = {'synonyms': synonyms}
        
        return self.main(self.request, self.template, ctx)

# setup the object, and decorate so that only logged in users can see it
SynonymsView = SynonymsView._decorate(login_required)


class SynonymEditView(ClassView):

    def __call__(self):
        
        ctx = {}
        
        child = False
        
        if 'parent_id' in self.kwargs:
            child = True
            try:
                parent_synonym = Synonym.objects.get(pk=self.kwargs['parent_id'])     
            except Synonym.DoesNotExist as e:
                return redirect('synonyms_list')
            

        if 'synonym_id' in self.kwargs:
            try:
                synonym = Synonym.objects.get(pk=self.kwargs['synonym_id'])     
            except Synonym.DoesNotExist as e:
                return redirect('synonyms_list')
        else:
            if child:
                synonym = Synonym(parent=parent_synonym)
            else:
                synonym = Synonym()
            
        form = SynonymForm(self.request.POST or None, instance=synonym)
      
        if self.request.method == 'POST' and form.is_valid():
            synonym = form.save()
            return redirect('synonyms_list')
        
        ctx['form'] = form
        ctx['synonym'] = synonym
                
        return self.main(self.request, self.template, ctx)

# setup the object, and decorate so that only logged in users can see it
SynonymEditView = SynonymEditView._decorate(login_required)

class SynonymRemoveView(ClassView):

    def __call__(self):

        if 'synonym_id' in self.kwargs:
            try:
                Synonym.objects.get(pk=self.kwargs['synonym_id']).delete()   
            except Synonym.DoesNotExist as e:
                return redirect('synonyms_list')
        
        return redirect('synonyms_list')
          


# setup the object, and decorate so that only logged in users can see it
SynonymRemoveView = SynonymRemoveView._decorate(login_required)

class SettingsView(ClassView):

    def __call__(self):
        
        ctx = {}

        tagfields = TagField.objects.all()

        if self.request.method == u'POST':
            tagfield_form = TagFieldForm(self.request.POST, prefix='settings')
            if tagfield_form.is_valid():
                tagfield = tagfield_form.save()
        else:
            tagfield_form = TagFieldForm(prefix='settings')      
        
        
        ctx = {u'tagfields': tagfields, u'tagfield_form': tagfield_form}
        return self.main(self.request, self.template, ctx)

# setup the object, and decorate so that only logged in users can see it
SettingsView = SettingsView._decorate(login_required)

class GenericAppView(ClassView):
    """ Show the page. Add your python code here to show dynamic content or feed information in
        to external apps
    """
    def __call__(self):
        # __call__ responds to the incoming request. It will already have a information associated to it, such as self.template and self.request

        log.debug("%s Viewing page" % self.request.user)
        ctx = {}
        
        # return a response to the request
        return self.main(self.request, self.template, ctx)

# setup the object, and decorate so that only logged in users can see it
GenericAppView = GenericAppView._decorate(login_required)
