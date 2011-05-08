from zope.app.component.hooks import getSite
import transaction
from Products.CMFCore.utils import getToolByName


def addInitialContent(context):
    '''
    Set up the initial IA for a plone conference web site
    '''
    if context.readDataFile('ploneconf.content.install.txt') is None:
        return
    
    # id: title
    pages = {   'training' : 'Training',
                'talks' : 'Talks',
                'open-spaces' : 'Open Spaces',
                'sprints' : 'Sprints',
                'sponsor' : 'Sponsors',
                'why-attend': 'Why Attend',
                'venue' : 'Venue',
                'travel' : 'Travel Info',
                'lodging' : 'Lodging',
                'location-details' : 'San Francisco',
                'performances' : 'Performances',
                'sponsors' : 'Sponsors',
                'volunteer' : 'Volunteer',
                'mission' : 'Mission',
            }
    
    # TODO: each folder will also have a home page
    folders = { 'event': 'Event',
                'location-info': 'Location',
                'party': 'Party',
                'register': 'Register',
                'about': 'About',
                } 
                
    # we should combine these into a mega structure at some point  
    # after the dust has settled 
    folderContentsMap = { 'event' : [  'training', 'talks', 'open-spaces', 
                                    'sprints', 'sponsor', 'why-attend',
                                  ],
                       'location-info': ['venue', 'travel', 'lodging', 
                                    'location-details', 
                                   ],
                       'party': [ 'performances', 'sponsors',
                                ],
                       'register': [],
                       'about': [ 'volunteer', 'mission',
                                ],
                       'legal': [],
                    }
                
    
    site = context.getSite()
    workflowTool = getToolByName(site, "portal_workflow")
    # add default pages and folders
    for id, title in folders.items():
        if not site.get(id):
            transaction.begin()
            site.manage_addFolder(id, title=title)
            folder = site.get(id)
            workflowTool.doActionFor(folder, "publish")
            transaction.commit()
        # TODO: add a home page if it doesn't exist and set 
        # the default view to be that page
        for page in folderContentsMap[id]:
            if page in pages:
                folder = site.get(id)
                if not folder.get(page):
                    transaction.begin()
                    portal_types = getToolByName(folder, "portal_types")
                    type_info = portal_types.getTypeInfo("Document")
                    pageObj = type_info._constructInstance(folder, page)
                    # TODO: set the title
                    workflowTool.doActionFor(pageObj, "publish")
                    transaction.commit()
                    
                    
        
        
def uninstall(context):
    if context.readDataFile('ploneconf.content.uninstall.txt') is None:
        return

    # currently we don't need anything but feel free to add stuff 
    # in the future