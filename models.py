from django.db import models

class Synonym(models.Model):
    value = models.CharField(max_length=255)
    parent = models.ForeignKey("self", related_name="synonyms", max_length=100, on_delete=models.CASCADE, blank=True, null=True)

class TagField(models.Model):
    fieldname = models.CharField(max_length=255)



from portal.plugins.synonyms.plistner import item_post_modify_handler