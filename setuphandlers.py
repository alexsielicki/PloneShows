# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2013 by unknown <unknown>
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('PloneShows: setuphandlers')
from Products.PloneShows.config import PROJECTNAME
from Products.PloneShows.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
##/code-section HEAD

def isNotPloneShowsProfile(context):
    return context.readDataFile("PloneShows_marker.txt") is None

def setupHideMetaTypesFromNavigations(context):
    """hide selected classes in the search form"""
    if isNotPloneShowsProfile(context): return 
    # XXX use https://svn.plone.org/svn/collective/DIYPloneStyle/trunk/profiles/default/properties.xml
    site = context.getSite()
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    for klass in ['Season', 'Now_Playing_Page']:
        propertyid = 'metaTypesNotToList'
        lines = list(navtreeProperties.getProperty(propertyid) or [])
        if klass not in lines:
            lines.append(klass)
            navtreeProperties.manage_changeProperties(**{propertyid: lines})



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotPloneShowsProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotPloneShowsProfile(context): return
    site = context.getSite()



##code-section FOOT
##/code-section FOOT
