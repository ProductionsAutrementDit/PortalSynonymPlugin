# PortalSynonymPlugin

This plugin allows you to set a number of synonyms for a tag type field.
Whenever the metadata of an item is changed, each entry in the predefined tag field is analyzed, and if it matches a synonym, replace the preset value.


## Installation

Place the plugin's file in a "synonym" folder in /opt/cantemo/portal/portal/plugins.  
In the plistner.py file, change the TAGS_FIELD value by the machine name of your tag field.

In shell, type:  
cd /opt/cantemo/portal/  
./manage.py schemamigration synonyms --initial  
./manage.py migrate synonyms  


## Configuration

Go to http://\<Yourserverurl\>/synonyms/admin/ or click in the "Synonym" menu item, under "Admin".  
Click on "Add new synonym" to add a new term.  
Click on "Add" to add a synonym to this term. Each synonyms will be replaced by the parent term.


## TODO
1. Add a settings page, with a dropdown to choose the tag field to inspect.
2. Allow to inspect multiple tag fields
3. Add a function to inspect all Portal elements and replace synonyms (can be very long)
