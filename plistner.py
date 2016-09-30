import logging
log = logging.getLogger(__name__)

from django.conf import settings

from portal.vidispine.iitem import ItemHelper
from VidiRest.helpers.vidispine import createMetadataDocumentFromDict

from portal.plugins.synonyms.models import Synonym, TagField

def synonyms_item_post_modify_handler(instance, method, **kwargs):
    if method == 'setItemMetadata':
        
        ith = ItemHelper()
        
        item = ith.getItem(instance)
        
        groups = ith.getItemMetadataFieldGroups(instance)
        group = groups['uri'][0]

        tag_fields = TagField.objects.all()
        

        _metadata = {u'fields': {}}
        
        for tag_field in tag_fields:
            
            change = False
        
            system_tag_field = item.getMetadataFieldByName(tag_field.fieldname)
            tags = system_tag_field.getFieldValues()

            new_values = []
            
            for tag in tags:
                try:
                    synonym = Synonym.objects.get(value=tag, parent__isnull=False)
                    parent_synonym = synonym.parent
                    change = True
                    new_values.append(parent_synonym.value) 
                    log.debug("Synonyms: modified tag field %s value from %s to %s" % (tag_field.fieldname, tag, parent_synonym.value))
                except Synonym.DoesNotExist as e:
                    new_values.append(tag)
            
            if change:
                _metadata[u'fields'][tag_field.fieldname] = {u'type': u'tags', u'value': new_values}
        
        
        if len(_metadata[u'fields']) > 0:
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


    