"""
This is your new plugin handler code.

Put your plugin handling code in here. remember to update the __init__.py file with 
you app version number. We have automatically generated a GUID for you, namespace, and a url 
that serves up index.html file
"""
import logging

from portal.pluginbase.core import Plugin, implements
from portal.generic.plugin_interfaces import (IPluginURL, IPluginBlock, IAppRegister, IPluginBootstrap)

log = logging.getLogger(__name__)

class SynonymsPluginURL(Plugin):
    """ Adds a plugin handler which creates url handler for the index page """
    implements(IPluginURL)

    def __init__(self):
        self.name = "Synonyms App"
        self.urls = 'portal.plugins.synonyms.urls'
        self.urlpattern = r'^synonyms/'
        self.namespace = r'synonyms'
        self.plugin_guid = '3ec88823-7756-4474-87d6-1e651d1e5b03'
        log.debug("Initiated Synonyms App")

pluginurls = SynonymsPluginURL()

# Create a menu item for ingest in the ingest section in the navbar
class SynonymstMenuNavigationPlugin(Plugin):
    implements(IPluginBlock)

    def __init__(self):
        self.name = "NavigationManagePlugin"
        self.plugin_guid = "adb62a9f-6863-497b-957a-63a7daebac3d"

    def return_string(self, tagname, *args):
        return {'guid': self.plugin_guid, 'template': 'synonyms/menuitem.html'}

navbarplugin = SynonymstMenuNavigationPlugin()


class SynonymsAdminNavigationPlugin(Plugin):
    # This adds your app to the navigation bar
    # Please update the information below with the author etc..
    implements(IPluginBlock)

    def __init__(self):
        self.name = "NavigationAdminPlugin"
        self.plugin_guid = 'b2b0b911-97a9-4169-9f93-ae30c5d70e88'
        log.debug('Initiated navigation plugin')

    # Returns the template file navigation.html
    # Change navigation.html to the string that you want to use
    def return_string(self, tagname, *args):
        return {'guid': self.plugin_guid, 'template': 'synonyms/navigation.html'}

navplug = SynonymsAdminNavigationPlugin()

class SynonymsAdminMenuPlugin(Plugin):
    u""" adds a menu item to the admin screen
    """
    implements(IPluginBlock)

    def __init__(self):
        self.name = 'AdminLeftPanelBottomPanePlugin'
        self.plugin_guid = 'feb066f1-7383-4669-bd13-73211e884394'

    def return_string(self, tagname, *args):
        return {'guid': self.plugin_guid, 'template': 'synonyms/admin/admin_leftpanel_pane.html'}

pluginblock = SynonymsAdminMenuPlugin()

class SynonymsRegister(Plugin):
    # This adds it to the list of installed Apps
    # Please update the information below with the author etc..
    implements(IAppRegister)

    def __init__(self):
        self.name = "Synonyms Registration App"
        self.plugin_guid = '84b5c2d5-28c6-402b-95c5-a5b1b4d2bcba'
        log.debug('Register the App')

    def __call__(self):
        from __init__ import __version__ as versionnumber
        _app_dict = {
                'name': 'Synonyms',
                'version': '0.0.1',
                'author': 'Camille Darley - Productions Autrement Dit',
                'author_url': 'www.pad.fr',
                'notes': 'Copyright 2016. All Rights Reserved.'}
        return _app_dict

synonymsplugin = SynonymsRegister()


class SynonymsBootstrap(Plugin):

    implements(IPluginBootstrap)

    def bootstrap(self):
        from portal.plugins.synonyms.plistner import synonyms_item_post_modify_handler
        from portal.vidispine.signals import vidispine_post_modify, vidispine_post_create
    
        vidispine_post_modify.connect(synonyms_item_post_modify_handler)
        vidispine_post_create.connect(synonyms_item_post_modify_handler)

SynonymsBootstrap()