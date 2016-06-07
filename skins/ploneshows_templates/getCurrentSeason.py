## Script (Python) "getCurrentSeason"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=return the latest published Season as a brain
##

from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot

catalog = getToolByName(context, 'portal_catalog')
limit = 1
state = 'published'
path = getNavigationRoot(context)
seasonBrain = None
# Gets seasons based on their effective data, 
# filters only the ones whose effective dates are in the past, meaning their publish date has already passed,
# sorts by effective date so the one that has been published most recently comes out on top,
# and limits the restults to only the top 1.
brains = catalog(portal_type='Season',
               review_state=state,
               effective={'query': DateTime(), 'range': 'max'},
               path=path,
               sort_on='effective',
               sort_order='descending',
               sort_limit=limit)[:limit]
if brains:
    seasonBrain = brains[0]
    
return seasonBrain