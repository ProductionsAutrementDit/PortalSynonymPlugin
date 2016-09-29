import logging
log = logging.getLogger(__name__)

from django.conf import settings

from portal.vidispine.iitem import ItemHelper
from VidiRest.helpers.vidispine import createMetadataDocumentFromDict

from portal.plugins.synonyms.models import Synonym
from portal.vidispine.signals import vidispine_post_modify, vidispine_post_create, vidispine_pre_modify

TAGS_FIELD = 'portal_mf245404'

def item_post_modify_handler(instance, method, **kwargs):
    if method == 'setItemMetadata':
        
        ith = ItemHelper()
        
        item = ith.getItem(instance)
        
        groups = ith.getItemMetadataFieldGroups(instance)
        group = groups['uri'][0]
        
        tags_field = item.getMetadataFieldByName(TAGS_FIELD)
        tags = tags_field.getFieldValues()
        
        new_values = []
        change = False
        
        for tag in tags:
            try:
                synonym = Synonym.objects.get(value=tag, parent__isnull=False)
                parent_synonym = synonym.parent
                change = True
                new_values.append(parent_synonym.value) 
                log.debug("Synonyms: modified tag from %s to %s" % (tag, parent_synonym.value))
            except Synonym.DoesNotExist as e:
                new_values.append(tag)
                
        
        if change:

            _metadata = {u'fields': {}}
            _metadata[u'fields'][TAGS_FIELD] = {u'type': u'tags', u'value': new_values}
            
            mfg_fields = None
            
            metadata_document = createMetadataDocumentFromDict(_metadata, [group], mfg_fields, settings.TIME_ZONE)
            
            ith.setItemMetadata(instance, metadata_document, skipForbidden=True, return_format='xml')

'''
def item_pre_modify_handler(instance, method, metadata_document, **kwargs):
    if method == 'setItemMetadata':
        
        ith = ItemHelper()
        
        item = ith.getItem(instance)
        
        if 'metadata_document' in kwargs:
            metadata_document = kwargs['metadata_document']

            
            for timespan in metadata_document.timespan:
                if timespan.start == '-INF' and timespan.end == '+INF':
                    for field in timespan.field:
                        if field.name == TAGS_FIELD:
                            for value in field.value_:
                                new_value = value.value().replace('test', 'test2')
                                value = VSXMLSchema.MetadataValueType(new_value)
            
            groups = ith.getItemMetadataFieldGroups(instance)
            group = groups['uri'][0]
            
            tags_field = item.getMetadataFieldByName(TAGS_FIELD)
            tags = tags_field.getFieldValues()
    
        #log.info("Synonyms: pre created/modified metadata: %s" % tags)
        #log.info("Synonyms: pre created/modified kwargs: %s" % kwargs)
'''

    
vidispine_post_modify.connect(item_post_modify_handler)
#vidispine_post_create.connect(item_post_modify_handler)
#vidispine_pre_modify.connect(item_pre_modify_handler)


    