## Script (Python) "getPreviousUnexpiredSeasons"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=return the the latest previous unexpired season and its upcoming performances
##

from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot

catalog = getToolByName(context, 'portal_catalog')
limit = 1
state = 'published'
path = getNavigationRoot(context)
seasonAndShows = None

# Gets seasons based on their effective data, 
# filters only the ones whose effective dates are in the past, meaning their publish date has already passed,
# sorts by effective date so the one that has been published most recently comes out on top,
# and limits the restults to only the top 1.
catalogFilter = {'portal_type':'Season',
               'review_state':state,
               'effective':{
                   # Published before current object minus 1 minute (1 second doesn't work). 
                   # Otherwise it includes the current object too.
                   'query': context.effective()-(1.0/24/60),
                   'range': 'max'}, 
               'expires':{'query': DateTime(), 'range': 'min'}, # Must not be expired
               'path':path,
               'sort_on':'effective',
               'sort_order':'descending',
               'sort_limit':limit,
    }
brains = catalog(catalogFilter)[:limit]

if brains:
    seasonBrain = brains[0]
    seasonObject = seasonBrain.getObject()
    shows = seasonObject.getFolderContents()
    showsWithUpcomingPerformances = [show.getObject() for show in shows if show.getObject().getUpcomingPerformances()]
    seasonAndShows = {'season':seasonObject, 'shows':showsWithUpcomingPerformances}
        
return seasonAndShows