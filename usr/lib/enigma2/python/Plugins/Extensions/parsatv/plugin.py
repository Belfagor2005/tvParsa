#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             09/06/2021               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function#, unicode_literals
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.Console import Console as iConsole
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.InfoBar import MoviePlayer, InfoBar
from Screens.InfoBarGenerics import *
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import *
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, fileExists
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import RT_HALIGN_LEFT, getDesktop, RT_HALIGN_RIGHT, RT_HALIGN_CENTER
from enigma import eTimer, eListboxPythonMultiContent, eListbox, eConsoleAppContainer, gFont
from os import path, listdir, remove, mkdir, chmod
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import glob
import os
import re
import shutil
import six
import ssl
import sys

global isDreamOS
global pngs
try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None

isDreamOS = False
try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

PY3 = sys.version_info.major >= 3
print('Py3: ',PY3)
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import Request
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import urlretrieve
from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import parse_qs
from six.moves.urllib.request import build_opener
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.parse import unquote_plus
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import urlencode
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error

global downloadparsa
downloadparsa = None
try:
    from Components.UsageConfig import defaultMoviePath
    downloadparsa = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadparsa = ('/media/hdd/movie/')
if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None
def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)
try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None
try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False
if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt

def checkInternet():
    try:
        response = checkStr(urlopen("http://google.com", None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True

def getUrl(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        response = urlopen(req)
        link = response.read()
        response.close()
        # print("link =", link)
        return link
    except:
        e = URLError
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)
        file_write.close()

def web_info(message):
    try:
        message = quote_plus(str(message))
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' 2>/dev/null &" % message
        debug(cmd, "CMD -> Console -> WEBIF")
        os.popen(cmd)
    except:
        print("web_info ERROR")

def ReloadBouquet():
    try:
        eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()
    except:
        os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')

DESKHEIGHT = getDesktop(0).size().height()
currversion = '1.3'
title_plug = 'Parsa TV '
desc_plugin = ('..:: Parsa TV by Lululla %s ::.. ' % currversion)
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
res_plugin_path=plugin_path + '/res/'
pngs=res_plugin_path + 'pics/setting.png'
pluglogo=res_plugin_path + 'pics/logo.png'
HD = getDesktop(0).size()
if HD.width() > 1280:
    skin_path=res_plugin_path + 'skins/fhd/'
else:
    skin_path=res_plugin_path + 'skins/hd/'
if isDreamOS:
    skin_path=skin_path + 'dreamOs/'

Panel_Dlist = [
 ('PARSA SPORT'),
 ('PARSA TV')
 ]

class MainParsaList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))
        if HD.width() > 1280:
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(50)

def DListEntry(name, idx):
    res = [name]
    if HD.width() > 1280:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1900, 50), font = 7, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if HD.width() > 1280:
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(22)
            self.l.setFont(0, gFont('Regular', textfont))

def OneSetListEntry(name):
    res = [name]
    if HD.width() > 1280:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1200, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 6), size = (34, 25), png = loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT))
    return res

def showlistpars(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(OneSetListEntry(name))
        icount = icount+1
        list.setList(plist)

class MainParsa(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainParsa')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self['text'] = MainParsaList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(title_plug)
        self['info'] = Label('')
        self['info'].setText(_('Please select ...'))
        self['key_yellow'] = Button(_(''))
        self['key_yellow'].hide()
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def closerm(self):
        self.close()

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_Dlist:
            list.append(DListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == _('PARSA SPORT'):
            self.session.open(parsasport)
        elif sel == _('PARSA TV'):
            self.session.open(parsatv)

class parsasport(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Parsa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = 'Parsa Sport'
        # self.url = 'http://www.parsatv.com/m/name=Varzesh-TV#persian'
        self.url ='http://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        self["key_blue"] = Button(_(''))
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'yellow': self.convert,
         'cancel': self.close}, -2)

    def convert2(self, result):
        if result:
            name= self.name
            self.make_m3u()

    def convert(self):
            self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?")% self.name, MessageBox.TYPE_YESNO, timeout = 15, default = True)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        items = []
        url = self.url
        name = self.name
        device = downloadparsa
        xxxname = device + 'ParsaSport.m3u'
        print('path device file ', xxxname)
        if os.path.exists(xxxname):
            print('permantly remove file ', xxxname)
            os.remove(xxxname)
        with open(xxxname, 'w') as e:
            e.write("#EXTM3U\n")
            content = getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            # print("content B =", content)
            n1 = content.find('channels">', 0)
            n2 = content.find("</table>", n1)
            content = content[n1:n2]
            regexvideo = '<li><a href="(.*?)"><button.*?myButton">(.*?)</button'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            # print("getVideos match =", match)
            for url, name in match:
                if 'sport' in str(url).lower():
                    name1 = name.replace('%20', ' ')
                    # print("getVideos15 name =", name1)
                    # print("getVideos15 url =", url)
                    item = name + "###" + url
                    items.append(item)
                    #save m3u
                    e.write('#EXTINF:-1,' + name1 +'\n')
                    e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                    content = getUrl(url)
                    if PY3:
                        content = six.ensure_str(content)
                    # print("content B =", content)
                    n1 = content.find('class="myButton" id=', 0)
                    n2 = content.find("</button></a>", n1)
                    content = content[n1:n2]
                    regexvideo = '<a href="(.*?)"><b'
                    match = re.compile(regexvideo,re.DOTALL).findall(content)
                    # print("getVideos match =", match)
                    for url2 in match:
                        url2 = url2
                        e.write(url2+'\n')
                    #save m3u end
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
            self['info'].setText(_('Please select ...'))
            showlistpars(self.names, self['text'])

    def make_m3u(self):
        namex = self.name
        name = 'sport'
        url = ''
        device = downloadparsa
        xxxname2 = device + 'Parsa2.m3u'
        if os.path.exists(xxxname2):
            print('permantly remove file ', xxxname2)
            os.remove(xxxname2)
        xxxname = device + 'ParsaSport.m3u'
        # print('path device file ', xxxname)
        if not os.path.exists(xxxname):
            return
        with open(xxxname2, 'w') as e:
            e.write("#EXTM3U\n")
            file_read = open(xxxname).readlines()
            for line in file_read:
                if line.startswith('#EXTINF'):
                    name = '%s' % line.split(',')[-1]
                    name = name.replace('%20', ' ').rstrip ('\n')
                elif line.startswith("http"):
                    url =line
                    # print("getVideos5 name =", name)
                    # print("getVideos5 url =", url)
                    e.write('#EXTINF:-1,' + name +'\n')
                    e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                    e.write(url+'\n')
        convert_bouquet(namex)

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            content = getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            # print("content B =", content)
            n1 = content.find('class="myButton" id=', 0)
            n2 = content.find("</button></a>", n1)
            content = content[n1:n2]
            regexvideo = '<a href="(.*?)"><b'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            # print("getVideos match =", match)
            for url in match:
                # url = url.replace('https','http')
                name = name
                pic = ''
                print("getVideos15 name =", name)
                print("getVideos15 url =", url)
                self.session.open(Playgo, name, url)
        except:
            print('error: ')
            pass

class parsatv(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Parsa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = 'Parsa Tv'
        self.url = 'https://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        self["key_blue"] = Button(_(''))
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'yellow': self.convert,
         'cancel': self.close}, -2)

    def convert2(self, result):
        if result:
            name= self.name
            self.make_m3u()

    def convert(self):
            self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?\n\nAttention!! Wait more than 5 minutes!!! ")% self.name, MessageBox.TYPE_YESNO, timeout = 15, default = True)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        items = []
        device = downloadparsa
        xxxname = device + 'ParsaTV.m3u'
        print('path device file ', xxxname)
        if os.path.exists(xxxname):
            print('permantly remove file ', xxxname)
            os.remove(xxxname)
        with open(xxxname, 'w') as e:
            e.write("#EXTM3U\n")
            url = self.url
            name = self.name
            content = getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            # print("content B =", content)
            n1 = content.find('channels">', 0)
            n2 = content.find("</table>", n1)
            content = content[n1:n2]
            regexvideo = '<li><a href="(.*?)"><button.*?myButton">(.*?)</button'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            # print("getVideos match =", match)
            for url, name in match:
                # url = url.replace('https','http')
                name1 = name.replace('%20', ' ')
                # print("getVideos15 name =", name1)
                # print("getVideos15 url =", url)
                item = name + "###" + url
                items.append(item)
                e.write('#EXTINF:-1,' + name1 +'\n')
                e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                e.write(url+'\n')
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
            self['info'].setText(_('Please select ...'))
            showlistpars(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            content = getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            # print("content B =", content)
            n1 = content.find('class="myButton" id=', 0)
            n2 = content.find("</button></a>", n1)
            content = content[n1:n2]
            regexvideo = '<a href="(.*?)"><b'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            # print("getVideos match =", match)
            for url in match:
                # url = url.replace('https','http')
                name = name
                pic = ''
                # print("getVideos15 name =", name)
                # print("getVideos15 url =", url)
                self.session.open(Playgo, name, url)
        except:
            print('error: ')
            pass

    def make_m3u(self):
        namex = self.name
        name = 'ParsaTv'
        url = ''
        device = downloadparsa
        xxxname2 = device + 'Parsa2.m3u'
        if os.path.exists(xxxname2):
            print('permantly remove file ', xxxname2)
            os.remove(xxxname2)
        xxxname = device + 'ParsaTV.m3u'
        print('path device file ', xxxname)
        if not os.path.exists(xxxname):
            return
        with open(xxxname2, 'w') as e:
            e.write("#EXTM3U\n")
            file_read = open(xxxname).readlines()
            for line in file_read:
                if line.startswith('#EXTINF'):
                    name = '%s' % line.split(',')[-1]
                    name = name.replace('%20', ' ').rstrip ('\n')
                elif line.startswith("http"):
                    url =line
                    content = getUrl(url)
                    if PY3:
                        content = six.ensure_str(content)
                    # print("content B =", content)
                    n1 = content.find('class="myButton" id=', 0)
                    n2 = content.find("</button></a>", n1)
                    content = content[n1:n2]
                    regexvideo = '<a href="(.*?)"><b'
                    match = re.compile(regexvideo,re.DOTALL).findall(content)
                    # print("getVideos match =", match)
                    for url in match:
                        if url.startswith("http"):
                            url=url
                        else:
                            url = 'http://www.parsatv.com' + url
                            content = getUrl(url)
                            if PY3:
                                content = six.ensure_str(content)
                            # print("content B =", content)
                            n1 = content.find('class="myButton" id=', 0)
                            n2 = content.find("</button></a>", n1)
                            content = content[n1:n2]
                            regexvideo = '<a href="(.*?)"><b'
                            match = re.compile(regexvideo,re.DOTALL).findall(content)
                            for url in match:
                                url=url
                    # print("getVideos5 name =", name)
                    # print("getVideos5 url =", url)
                    e.write('#EXTINF:-1,' + name +'\n')
                    e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                    e.write(url+'\n')
        convert_bouquet(namex)

class Playgo(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):

    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.skinName = 'MoviePlayer'
        title = 'Play'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self)
        InfoBarShowHide.__init__(self)
        self['actions'] = ActionMap(['WizardActions',
         'MoviePlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions'], {'leavePlayer': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        InfoBarSeek.__init__(self, actionmap='MediaPlayerSeekActions')
        url = url.replace(':', '%3a')
        self.url = url
        self.name = name
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)

    def openTest(self):
        url = self.url
        name = self.name
        print("Here in Playvid name A =", name)
        name = name.replace(":", "-")
        name = name.replace("&", "-")
        name = name.replace(" ", "-")
        name = name.replace("/", "-")
        name = name.replace("›", "-")
        name = name.replace(",", "-")
        print("Here in Playvid name B2 =", name)
        if url is not None:
            url = str(url)
            url = url.replace(":", "%3a")
            url = url.replace("\\", "/")
            print("url final= ", url)
            ref = "4097:0:1:0:0:0:0:0:0:0:" + url
            print("ref= ", ref)
            sref = eServiceReference(ref)
            sref.setName(self.name)
            self.session.nav.stopService()
            self.session.nav.playService(sref)
        else:
           return

    def openTestX(self):
        ref = '4097:0:1:0:0:0:0:0:0:0:' + self.url
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefOld)
        self.close()

    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def keyNumberGlobal(self, number):
        self['text'].number(number)

def convert_bouquet(namex):
    device = downloadparsa
    xxxname = device + 'Parsa2.m3u'
    print('path device file ', xxxname)
    name = namex.replace(' ','').lower()
    if not os.path.exists(xxxname):
        self.mbox = self.session.open(openMessageBox, _('Check %sParsa2.m3u') %device, openMessageBox.TYPE_INFO, timeout=5)
        return
    parsabouquet = 'userbouquet.%s.tv' % name
    desk_tmp = ''
    in_bouquets = 0
    if os.path.isfile('/etc/enigma2/%s' % parsabouquet):
            os.remove('/etc/enigma2/%s' % parsabouquet)
    with open('/etc/enigma2/%s' % parsabouquet, 'w') as outfile:
        outfile.write('#NAME %s\r\n' % name.capitalize())
        for line in open(xxxname ):
            if line.startswith('http://') or line.startswith('https'):
                outfile.write('#SERVICE 4097:0:1:1:0:0:0:0:0:0:%s' % line.replace(':', '%3a'))
                outfile.write('#DESCRIPTION %s' % desk_tmp)
            elif line.startswith('#EXTINF'):
                desk_tmp = '%s' % line.split(',')[-1]
            elif '<stream_url><![CDATA' in line:
                outfile.write('#SERVICE 4097:0:1:1:0:0:0:0:0:0:%s\r\n' % line.split('[')[-1].split(']')[0].replace(':', '%3a'))
                outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
            elif '<title>' in line:
                if '<![CDATA[' in line:
                    desk_tmp = '%s\r\n' % line.split('[')[-1].split(']')[0]
                else:
                    desk_tmp = '%s\r\n' % line.split('<')[1].split('>')[1]
        outfile.close()
        message = (_("Wait please... "))
        web_info(message)
    if os.path.isfile('/etc/enigma2/bouquets.tv'):
        for line in open('/etc/enigma2/bouquets.tv'):
            if parsabouquet in line:
                in_bouquets = 1

        if in_bouquets == 0:
            if os.path.isfile('/etc/enigma2/%s' % parsabouquet) and os.path.isfile('/etc/enigma2/bouquets.tv'):
                remove_line('/etc/enigma2/bouquets.tv', parsabouquet)
                with open('/etc/enigma2/bouquets.tv', 'a') as outfile:
                    outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % parsabouquet)
                    outfile.close()
    message = (_("Bouquet converted successful"))
    web_info(message)
    ReloadBouquet()

def main(session, **kwargs):
    if checkInternet():
        session.open(MainParsa)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

def StartSetup(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('Parsa TV'), main, 'Parsa TV', 15)]
    else:
        return []

def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not isDreamOS:
        ico_path = plugin_path + '/res/pics/logo.png'
    extensions_menu = PluginDescriptor(name = title_plug, description = desc_plugin, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main, needsRestart = True)
    result = [PluginDescriptor(name = title_plug, description = desc_plugin, where = PluginDescriptor.WHERE_PLUGINMENU, icon = ico_path, fnc = main)]
    result.append(extensions_menu)
    return result

def decodeUrl(text):
	text = text.replace('%20',' ')
	text = text.replace('%21','!')
	text = text.replace('%22','"')
	text = text.replace('%23','&')
	text = text.replace('%24','$')
	text = text.replace('%25','%')
	text = text.replace('%26','&')
	text = text.replace('%2B','+')
	text = text.replace('%2F','/')
	text = text.replace('%3A',':')
	text = text.replace('%3B',';')
	text = text.replace('%3D','=')
	text = text.replace('&#x3D;','=')
	text = text.replace('%3F','?')
	text = text.replace('%40','@')
	return text

def decodeHtml(text):
	text = text.replace('&auml;','ä')
	text = text.replace('\u00e4','ä')
	text = text.replace('&#228;','ä')
	text = text.replace('&oacute;','ó')
	text = text.replace('&eacute;','e')
	text = text.replace('&aacute;','a')
	text = text.replace('&ntilde;','n')

	text = text.replace('&Auml;','Ä')
	text = text.replace('\u00c4','Ä')
	text = text.replace('&#196;','Ä')

	text = text.replace('&ouml;','ö')
	text = text.replace('\u00f6','ö')
	text = text.replace('&#246;','ö')

	text = text.replace('&ouml;','Ö')
	text = text.replace('\u00d6','Ö')
	text = text.replace('&#214;','Ö')

	text = text.replace('&uuml;','ü')
	text = text.replace('\u00fc','ü')
	text = text.replace('&#252;','ü')

	text = text.replace('&Uuml;','Ü')
	text = text.replace('\u00dc','Ü')
	text = text.replace('&#220;','Ü')

	text = text.replace('&szlig;','ß')
	text = text.replace('\u00df','ß')
	text = text.replace('&#223;','ß')

	text = text.replace('&amp;','&')
	text = text.replace('&quot;','\"')
	text = text.replace('&quot_','\"')

	text = text.replace('&gt;','>')
	text = text.replace('&apos;',"'")
	text = text.replace('&acute;','\'')
	text = text.replace('&ndash;','-')
	text = text.replace('&bdquo;','"')
	text = text.replace('&rdquo;','"')
	text = text.replace('&ldquo;','"')
	text = text.replace('&lsquo;','\'')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&#034;','\'')
	text = text.replace('&#038;','&')
	text = text.replace('&#039;','\'')
	text = text.replace('&#39;','\'')
	text = text.replace('&#160;',' ')
	text = text.replace('\u00a0',' ')
	text = text.replace('&#174;','')
	text = text.replace('&#225;','a')
	text = text.replace('&#233;','e')
	text = text.replace('&#243;','o')
	text = text.replace('&#8211;',"-")
	text = text.replace('\u2013',"-")
	text = text.replace('&#8216;',"'")
	text = text.replace('&#8217;',"'")
	text = text.replace('#8217;',"'")
	text = text.replace('&#8220;',"'")
	text = text.replace('&#8221;','"')
	text = text.replace('&#8222;',',')
	text = text.replace('&#x27;',"'")
	text = text.replace('&#8230;','...')
	text = text.replace('\u2026','...')
	text = text.replace('&#41;',')')
	text = text.replace('&lowbar;','_')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&lpar;','(')
	text = text.replace('&rpar;',')')
	text = text.replace('&comma;',',')
	text = text.replace('&period;','.')
	text = text.replace('&plus;','+')
	text = text.replace('&num;','#')
	text = text.replace('&excl;','!')
	text = text.replace('&#039','\'')
	text = text.replace('&semi;','')
	text = text.replace('&lbrack;','[')
	text = text.replace('&rsqb;',']')
	text = text.replace('&nbsp;','')
	text = text.replace('&#133;','')
	text = text.replace('&#4','')
	text = text.replace('&#40;','')

	text = text.replace('&atilde;',"'")
	text = text.replace('&colon;',':')
	text = text.replace('&sol;','/')
	text = text.replace('&percnt;','%')
	text = text.replace('&commmat;',' ')
	text = text.replace('&#58;',':')

	return text
