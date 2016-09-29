from django.forms import ModelForm

from portal.plugins.synonyms.models import Synonym

# Create the form class.
class SynonymForm(ModelForm):
    class Meta:
        model = Synonym
        fields = ['value']