from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)

def install(portal):
    """Run the GS profile to install this package"""
    out = StringIO()
    runProfile(portal, 'profile-ploneconf.content:default')
    print >>out, "Installed ploneconf.content. You're welcome."
    return out.getvalue()
    
def beforeUninstall(portal, reinstall, product, cascade):
    # hook that makes sure we don't remove created content
    # this is patched in some version of plone although I'm 
    # not sure when it was released so I'll leave it for now
    # file under: lazy bum
    try:
        cascade.remove('portalobjects')
    except:
        ValueError
    return None, cascade

def uninstall(portal, reinstall=False):
    """Run the GS profile to uninstall this package"""
    out = StringIO()
    if not reinstall:
        runProfile(portal, 'profile-ploneconf.content:uninstall')
        print >>out, "Uninstalled ploneconf.content"
    return out.getvalue()