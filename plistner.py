import logging
log = logging.getLogger(__name__)

from django.conf import settings

from portal.vidispine.iitem import ItemHelper
from VidiRest.helpers.vidispine import createMetadataDocumentFromDict

from portal.plugins.synonyms.models import Synonym, TagField

def synonyms_item_pre_modify_handler(instance, method, **kwargs):
    if method == 'setItemMetadata':
    
        if 'metadata_document' in kwargs:
    
            import VidiRest.schemas.xmlSchema as VSXMLSchema
            
            log.debug("Call pre modify")
        
            tag_fields = TagField.objects.all()
            
            tag_fieldnames = []
            
            for tag_field in tag_fields:
                tag_fieldnames.append(tag_field.fieldname)         
                log.debug("Synonyms: get field names: %s" % tag_field.fieldname)
            

            for timespan_index, timespan in enumerate(kwargs['metadata_document'].timespan):
                log.debug("Found timespan")
                if timespan.start != '-INF' and timespan.end != '+INF':
                    log.debug("Timed timespan, skip")
                    continue
                for field_index, field in enumerate(timespan.field):
                    log.debug("Found field %s" % field.name)
                    if field.name not in tag_fieldnames:
                        continue
                    change = False
                    new_values = []
                    for value in field.value_:
                        log.debug("Found value %s" % value.value())
                        try:
                            synonym = Synonym.objects.get(value=value.value(), parent__isnull=False)
                            parent_synonym = synonym.parent
                            change = True
                            new_values.append(VSXMLSchema.MetadataValueType(parent_synonym.value))
                            log.debug("Synonyms: modified tag field %s value from %s to %s" % (field.name, value.value(), parent_synonym.value))
                        except Synonym.DoesNotExist as e:
                            log.debug("Synonyms: do not modify tag field %s value %s" % (field.name, value.value()))
                            new_values.append(VSXMLSchema.MetadataValueType(value.value()))
                    if change:
                        kwargs['metadata_document'].timespan[timespan_index].field[field_index].value_ = new_values



    