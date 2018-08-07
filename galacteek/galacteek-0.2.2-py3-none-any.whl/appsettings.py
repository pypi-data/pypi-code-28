
from PyQt5.QtCore import QCoreApplication, QUrl, QStandardPaths, QSettings

# Settings sections
CFG_SECTION_IPFSD = 'ipfsdaemon'
CFG_SECTION_IPFS = 'ipfs'
CFG_SECTION_BROWSER = 'browser'
CFG_SECTION_IPFSCONN1 = 'ipfsconn1'
CFG_SECTION_UI = 'ui'

CFG_KEY_ENABLED = 'enabled'

# These keys are for ipfsdaemon and ipfsconn sections
CFG_KEY_APIPORT = 'apiport'
CFG_KEY_SWARMPORT = 'swarmport'
CFG_KEY_HTTPGWPORT = 'httpgwport'
CFG_KEY_HOST = 'host'
CFG_KEY_SWARMLOWWATER = 'swarm_lowwater'
CFG_KEY_SWARMHIGHWATER = 'swarm_highwater'
CFG_KEY_STORAGEMAX = 'storagemax' # integer, max storage in Gb
CFG_KEY_CORS = 'cors'

# Browser
CFG_KEY_HOMEURL = 'homeurl'
CFG_KEY_GOTOHOME = 'gotohomeonnewtab'
CFG_KEY_DLPATH = 'downloadspath'
CFG_KEY_ALLOWHTTPBROWSING = 'httpbrowsing'
CFG_KEY_JSAPI = 'jsapi'

# IPFS
CFG_KEY_PUBSUB = 'pubsub'

# UI
CFG_KEY_WRAPSINGLEFILES = 'wrapsinglefiles'
CFG_KEY_WRAPDIRECTORIES = 'wrapdirectories'
CFG_KEY_HIDEHASHES = 'hidehashes'
CFG_KEY_LANG = 'lang'

# for fast access
S_HOMEURL = (CFG_SECTION_BROWSER, CFG_KEY_HOMEURL)
S_GOTOHOME = (CFG_SECTION_BROWSER, CFG_KEY_GOTOHOME)
S_DOWNLOADS_PATH = (CFG_SECTION_BROWSER, CFG_KEY_DLPATH)

def setDefaultSettings(gApp):
    # Sets the default settings
    sManager = gApp.settingsMgr

    section = CFG_SECTION_IPFSD
    sManager.setDefaultSetting(section, CFG_KEY_APIPORT, 5001)
    sManager.setDefaultSetting(section, CFG_KEY_SWARMPORT, 4001)
    sManager.setDefaultSetting(section, CFG_KEY_HTTPGWPORT, 8080)
    sManager.setDefaultSetting(section, CFG_KEY_SWARMHIGHWATER, 300)
    sManager.setDefaultSetting(section, CFG_KEY_SWARMLOWWATER, 150)
    sManager.setDefaultSetting(section, CFG_KEY_STORAGEMAX, 20)
    sManager.setDefaultTrue(section, CFG_KEY_CORS)
    sManager.setDefaultTrue(section, CFG_KEY_ENABLED)

    section = CFG_SECTION_BROWSER
    sManager.setDefaultSetting(section, CFG_KEY_HOMEURL, 'ipfs:/ipns/ipfs.io')
    sManager.setDefaultSetting(section, CFG_KEY_DLPATH,
        gApp.defaultDownloadsLocation)
    sManager.setDefaultTrue(section, CFG_KEY_GOTOHOME)
    sManager.setDefaultFalse(section, CFG_KEY_JSAPI)
    sManager.setDefaultFalse(section, CFG_KEY_ALLOWHTTPBROWSING)

    # Default IPFS connection when not spawning daemon
    section = CFG_SECTION_IPFSCONN1
    sManager.setDefaultSetting(section, CFG_KEY_HOST, 'localhost')
    sManager.setDefaultSetting(section, CFG_KEY_APIPORT, 5001)
    sManager.setDefaultSetting(section, CFG_KEY_HTTPGWPORT, 8080)

    section = CFG_SECTION_IPFS
    sManager.setDefaultFalse(section, CFG_KEY_PUBSUB)

    section = CFG_SECTION_UI
    sManager.setDefaultTrue(section, CFG_KEY_WRAPSINGLEFILES)
    sManager.setDefaultFalse(section, CFG_KEY_WRAPDIRECTORIES)
    sManager.setDefaultFalse(section, CFG_KEY_HIDEHASHES)
    sManager.setDefaultSetting(section, CFG_KEY_LANG, 'en')
    sManager.sync()
    return True

class SettingsManager(object):
    # QSettings has its problems with pyqt5 regarding booleans
    trueVal = 'true'
    falseVal = 'false'

    def __init__(self, path=None):
        self.settings = QSettings(path, QSettings.IniFormat)

    def sync(self):
        """ Synchronize settings to disk """
        return self.settings.sync()

    def eSet(self, key, value):
        """ Easy set. key is a (section, key) tuple """
        return self.setSetting(key[0], key[1], value)

    def eGet(self, key, type=None):
        """ Easy get. key is a (section, key) tuple """
        return self.getSetting(key[0], key[1], type=type)

    def setSetting(self, section, name, value):
        """ Changes a setting to given value

        :param str section: setting section
        :param str name: key inside the section
        :param value: setting value
        """
        self.settings.setValue('{0}/{1}'.format(section, name), value)

    def setDefaultSetting(self, section, name, value):
        """
        Sets default setting for section and name if that setting hasn't
        been registered yet
        """
        existing = self.getSetting(section, name)
        if not existing:
            self.settings.setValue('{0}/{1}'.format(section, name), value)

    def setDefaultTrue(self, section, name):
        return self.setDefaultSetting(section, name, self.trueVal)

    def setDefaultFalse(self, section, name):
        return self.setDefaultSetting(section, name, self.falseVal)

    def getInt(self, section, name):
        """
        Gets the setting referenced by section and name, casting it as
        an integer
        """
        return self.getSetting(section, name, type=int)

    def getSetting(self, section, name, type=None):
        """ Gets a setting, casting it to the given type

        :param str section: setting section
        :param str name: key inside the section
        :param type: type to convert to
        """
        key = '{0}/{1}'.format(section, name)
        if type:
            return self.settings.value(key, type=type)
        else:
            return self.settings.value(key)

    def setTrue(self, section, name):
        return self.setSetting(section, name, self.trueVal)

    def setFalse(self, section, name):
        return self.setSetting(section, name, self.falseVal)

    def setBoolFrom(self, section, name, boolVal):
        if boolVal is True:
            self.setTrue(section, name)
        elif boolVal is False:
            self.setFalse(section, name)

    def isTrue(self, section, name):
        return self.getSetting(section, name) == self.trueVal

    def isFalse(self, section, name):
        return self.getSetting(section, name) == self.falseVal

    # Properties

    @property
    def hideHashes(self):
        return self.isTrue(CFG_SECTION_UI, CFG_KEY_HIDEHASHES)

    @property
    def wrapFiles(self):
        return self.isTrue(CFG_SECTION_UI, CFG_KEY_WRAPSINGLEFILES)

    @property
    def wrapDirectories(self):
        return self.isTrue(CFG_SECTION_UI, CFG_KEY_WRAPDIRECTORIES)

    @property
    def allowHttpBrowsing(self):
        return self.isTrue(CFG_SECTION_BROWSER, CFG_KEY_ALLOWHTTPBROWSING)

    @property
    def jsIpfsApi(self):
        return self.isTrue(CFG_SECTION_BROWSER, CFG_KEY_JSAPI)
