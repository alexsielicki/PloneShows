# -*- coding: utf-8 -*-
#
# File: PloneShows.py
#
# Copyright (c) 2013 by unknown <unknown>
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "PloneShows"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'Season': 'PloneShows: Add Season',
    'Show': 'PloneShows: Add Show',
    'Performance': 'PloneShows: Add Performance',
    'Now_Playing_Page': 'PloneShows: Add Now_Playing_Page',
}

setDefaultRoles('PloneShows: Add Season', ('Manager','Owner'))
setDefaultRoles('PloneShows: Add Show', ('Manager','Owner'))
setDefaultRoles('PloneShows: Add Performance', ('Manager','Owner'))
setDefaultRoles('PloneShows: Add Now_Playing_Page', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.PloneShows.AppConfig import *
except ImportError:
    pass
