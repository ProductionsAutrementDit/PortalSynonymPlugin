# PortalSynonymPlugin

This plugin allows you to set a number of synonyms for a tag type field.
Whenever the metadata of an item is changed, each entry in the predefined tag field is analyzed, and if it matches a synonym, replace the preset value.


## Installation

Place the plugin's file in a "synonym" folder in /opt/cantemo/portal/portal/plugins.  

In shell, type:  
cd /opt/cantemo/portal/  
./manage.py schemamigration synonyms --initial  
./manage.py migrate synonyms  


## Configuration

Go to http://\<Yourserverurl\>/synonyms/admin/ or click in the "Synonym" menu item, under "Admin".  
Add as many tag fields as you need.   
Go to http://\<Yourserverurl\>/synonyms/ or click in the "Synonym" menu item, under "Manage". 
Click on "Add new synonym" to add a new term.  
Click on "Add" to add a synonym to this term. Each synonyms will be replaced by the parent term.


## Use

Edit an item metadata or create a new item.   
Upon item save, tag fields values are inspected and replaced by their synonym.

## TODO
1. Add a function to inspect all Portal elements and replace synonyms (can be very long)
