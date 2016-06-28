# -*- coding: utf-8 -*-
#
# File: Show.py
#
# Copyright (c) 2013 by unknown <unknown>
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.ATContentTypes.content.newsitem import ATNewsItemSchema
from Products.PloneShows.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.newsitem import ATNewsItemSchema

##code-section module-header #fill in your manual code here
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.document import ATDocumentBase
from DateTime import DateTime
from Products.ATContentTypes.configuration import zconf
from Products.validation import V_REQUIRED
from Products.ATContentTypes import ATCTMessageFactory as _
##/code-section module-header

copied_fields = {}
copied_fields['image'] = ATNewsItemSchema['image'].copy()
copied_fields['image'].sizes = {'large':(768, 768), 'wideheader':(637, 300), 'preview':(400, 400), 'mini':(200, 200), 'thumb':(128, 128), 'tile':(64, 64), 'icon':(32, 32), 'listing':(16, 16),}
copied_fields['image'].required = True
copied_fields['image'].widget.label = 'Header Image'
copied_fields['image'].widget.description = 'Horizontal header image displayed on show and performance pages.'
copied_fields['imageCaption'] = ATNewsItemSchema['imageCaption'].copy()
copied_fields['imageCaption'].widget.visible = 0
# copied_fields['imagePopejoySeasonListing'] = ATNewsItemSchema['image'].copy()
# copied_fields['imagePopejoySeasonListing'].name = 'imagePopejoySeasonListing'
# copied_fields['imagePopejoySeasonListing'].sizes = {'large':(768, 768), 'wideheader':(637, 300), 'preview':(400, 400), 'mini':(200, 200), 'thumb':(128, 128), 'tile':(64, 64), 'icon':(32, 32), 'listing':(16, 16),}
schema = Schema((

    DateTimeField(
        name='individualTixStartDate',
        widget=DateTimeField._properties['widget'](
            label="Individual Ticket Purchase Start Date",
            description="Date when visitors can start buying individual tickets.  Overrides the season's Individual Ticket Purchase Start Date.  Leave blank to use this date from the season. For a cancelled show, set this date to be after the show's last performance.",
            label_msgid='PloneShows_label_individualTixStartDate',
            description_msgid='PloneShows_help_individualTixStartDate',
            i18n_domain='PloneShows',
        ),
    ),
    StringField(
        name='individualTixLink',
        widget=StringField._properties['widget'](
            label="Individual Ticket Link URL",
            description="Link address for individual tickets",
            label_msgid='PloneShows_label_individualTixLink',
            description_msgid='PloneShows_help_individualTixLink',
            i18n_domain='PloneShows',
        ),
    ),
    copied_fields['image'],

    copied_fields['imageCaption'],

    ImageField(
        'imagePopejoyTallThumbnail',
        required=True,
        storage=AnnotationStorage(migrate=True),
        languageIndependent=True,
        max_size=zconf.ATNewsItem.max_image_dimension,
        sizes={'large': (768, 768),
               'tallthumbnail': (193, 260),
               'preview': (400, 400),
               'mini': (200, 200),
               'thumb': (128, 128),
               'tile': (64, 64),
               'icon': (32, 32),
               'listing': (16, 16),
               },
        validators=(('isNonEmptyFile', V_REQUIRED),
                    ('checkNewsImageMaxSize', V_REQUIRED)),
        widget=ImageWidget(
            description='Vertical thumbnail image displayed on season page and homepage.',
            label='Thumbnail Image',
            show_content_type=False)
    ),


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Show_schema = ATFolderSchema + ATNewsItemSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Show_schema.moveField('imagePopejoyTallThumbnail', after='image')
##/code-section after-schema

class Show(ATFolder, ATNewsItem):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IShow)

    meta_type = 'Show'
    _at_rename_after_creation = True

    schema = Show_schema

    ##code-section class-header #fill in your manual code here
    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.getImageCaption()
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATDocumentBase.__bobo_traverse__(self, REQUEST, name)

    ##/code-section class-header

    # Methods

    security.declarePublic('getUpcomingPerformances')
    def getUpcomingPerformances(self):
        """
        """
        return self.getFolderContents({ 'portal_type': 'Performance', 'sort_on': 'start', 'start': {'query': DateTime(), 'range': 'min'} })

    security.declarePublic('getPastPerformances')
    def getPastPerformances(self):
        """
        """
        return self.getFolderContents({ 'portal_type': 'Performance', 'sort_on': 'start', 'sort_order': 'descending', 'start': {'query': DateTime(), 'range': 'max'} })

    security.declarePublic('individualTixActive')
    def individualTixActive(self):
        """
        """
        active = False
        now = DateTime()
        startDate = self.getIndividualTixStartDateOrSeasons()
        if startDate and (now > startDate):
            active = True
        return active

    security.declarePublic('getIndividualTixStartDateOrSeasons')
    def getIndividualTixStartDateOrSeasons(self):
        """ returns the show's individualTixStartDate if it has one, otherwise returns the parent's (seson's)
        """
        individualTixStartDate = self.getIndividualTixStartDate()
        if not individualTixStartDate:
            individualTixStartDate = self.aq_inner.aq_parent.getIndividualTixStartDate()
        return individualTixStartDate

    # Manually created methods

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.getImageCaption()
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATDocumentBase.__bobo_traverse__(self, REQUEST, name)



registerType(Show, PROJECTNAME)
# end of class Show

##code-section module-footer #fill in your manual code here
##/code-section module-footer

