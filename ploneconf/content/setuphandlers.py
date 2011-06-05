import transaction
from Products.CMFCore.utils import getToolByName


def addInitialContent(context):
    '''
    Set up the initial IA for a plone conference web site
    '''
    if context.readDataFile('ploneconf.content.install.txt') is None:
        return

    site = context.getSite()

    # bye bye Plone's default content
    existing = site.keys()
    for n in ('events', 'front-page'):
        if n in existing:
            transaction.begin()
            del site[n]
            transaction.commit()

    # hide the Members folder
    if 'Members' in existing:
        transaction.begin()
        members = site['Members']
        members.getField('excludeFromNav').set(members, True)
        members.reindexObject()
        transaction.commit()

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
                'index_html'  : 'Home',
                'non-profit' : '501c3',
            }
    
    # TODO: each folder will also have a home page
    folders = { 'event': 'Event',
                'location-info': 'Location',
                'party': 'Party',
                'register': 'Register',
                'about': 'About',
                'legal': 'Legal',
                'slideshow-folder': 'Slideshow Folder',
                } 
                
    # we should combine these into a mega structure at some point  
    # after the dust has settled 
    folderContentsMap = { 'event' : ['index_html',  'training', 'talks', 'open-spaces', 
                                    'sprints', 'sponsor', 'why-attend',
                                    ],
                       'location-info': ['index_html', 'venue', 'travel', 'lodging', 
                                    'location-details', 
                                   ],
                       'party': [ 'index_html', 'performances', 'sponsors',],
                       'register': ['index_html'],
                       'about': [ 'index_html', 'volunteer', 'mission',
                                ],
                       'legal': [ 'index_html', 'non-profit'],
                    }
                
    
    workflowTool = getToolByName(site, "portal_workflow")
    # add default pages and folders
    for id, title in folders.items():
        if not site.get(id):
            transaction.begin()
            site.manage_addFolder(id, title=title)
            folder = site.get(id)
            workflowTool.doActionFor(folder, "publish")
            transaction.commit()
            if id in folderContentsMap:
                for page in folderContentsMap[id]:
                    if page in pages:
                        if not folder.get(page):
                            transaction.begin()
                            portal_types = getToolByName(folder, "portal_types")
                            type_info = portal_types.getTypeInfo("Document")
                            pageObj = type_info._constructInstance(folder, page,
                                                                    title=pages[page])
                            workflowTool.doActionFor(pageObj, "publish")
                            transaction.commit()
            # set the default view of the folder to be that
            # only do this after the home page has been created
            # XXX: somthing is missing here. WhyTF isn't this working
            # for now let's use index_html but at some point it might be wise 
            # to move away from that hackiness
            # folder.setDefaultPage("home")
            # folder.setLayout("home")
        
        
def uninstall(context):
    if context.readDataFile('ploneconf.content.uninstall.txt') is None:
        return

    # currently we don't need anything but feel free to add stuff 
    # in the future
