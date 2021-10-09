#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             10/09/2021               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function#, unicode_literals
from . import _
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
import socket
global pngs
global downloadparsa
downloadparsa = None
try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None
from random import choice
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import Request
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.parse import quote
ListAgent = [
          'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
          'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
          'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
          'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
          'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8',
          'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
          'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
          'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
          'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2',
          'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1',
          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
          'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',
          'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0a2) Gecko/20111101 Firefox/9.0a2',
          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2',
          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110612 Firefox/6.0a2',
          'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20110814 Firefox/6.0',
          'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
          'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
          'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
          'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
          'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
          'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
          'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
          'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;  it-IT)',
          'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)'
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)',
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)',
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.1; SV1; .NET CLR 2.8.52393; WOW64; en-US)',
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)',
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/4.0; GTB7.4; InfoPath.3; SV1; .NET CLR 3.1.76908; WOW64; en-US)',
          'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
          'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
          'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.8.36217; WOW64; en-US)',
          'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
          'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; it-IT)',
          'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
          'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
          'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
          'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00',
          'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
          'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
          'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0',
          'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
          'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3'
          ]

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

def RequestAgent():
    RandomAgent = choice(ListAgent)
    return RandomAgent

def checkStr(txt):
    if six.PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt

def convert_to_unicode(text):
    """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return six.ensure_text(text, "utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return six.ensure_text(text, "utf-8", "ignore")
        elif isinstance(text, six.text_type):
            return text
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")

def checkInternet():
    try:
        socket.setdefaulttimeout(5.0)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except:
        return False

def getUrl(url):
    link = []
    url = checkStr(url)
    print(  "Here in getUrl url =", url)
    req = Request(url)
    req.add_header('User-Agent',RequestAgent())
    try:
        response = urlopen(req)
        link=response.read()
        response.close()
        return link
    except:
        import ssl
        gcontext = ssl._create_unverified_context()
        response = urlopen(req, context=gcontext)
        link=response.read()
        response.close()
        return link

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
        message = quote_plus(message)
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' > /dev/null 2>&1 &" % message
        # debug(cmd, "CMD -> Console -> WEBIF")
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
currversion = '1.5'
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
if os.path.exists('/var/lib/dpkg/status'):
    skin_path=skin_path + 'dreamOs/'

Panel_Dlist = [
 ('PARSA ALL TV'),
 ('PARSA TV CATEGORY'),
 ('PARSA SPORT')
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
        elif sel == _('PARSA ALL TV'):
            self.session.open(parsatv)
        elif sel == _('PARSA TV CATEGORY'):
            self.session.open(parsatv2)
        else:
            return

class parsatv2(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('ParsaTV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = 'Parsa Sport'
        # self.url = 'http://www.parsatv.com/name=Varzesh-TV#persian'
        self.url = 'https://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()

        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         # 'yellow': self.convert,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        self.names = []
        self.urls = []
        items = []
        try:
            content = getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            n6 = content.find("<a></a></td>")
            if str(n6) in content:
                content.replace(str(n6),'<a></a></li></td>')
                print('yes is n6')
            else:
                print('no, no n6 in parsatv2!')
            regexvideo = '<tr>.*?<td id=".*?><li>(.+?)<a>.*?</td>.*?</tr>'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            for name in match:
                url = url.replace(' ','%20')
                name = name
                # print("parsatv2 name =", name)
                # print("parsatv2 url =", url)
                item = name + "###" + url
                items.append(item)
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
            self['info'].setText(_('Please select ...'))
            showlistpars(self.names, self['text'])
        except Exception as e:
            print('error parsatv2', e)

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(parsatv3, name, url)

class parsatv3(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Parsa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        self["key_blue"] = Button(_(''))
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'yellow': self.convert,
         'cancel': self.close}, -2)

    def convert2(self, result):
        if result:
            namex = self.name.lower()
            namex = namex.replace(' ','-')
            namex = namex.strip()
            if os.path.exists('/var/lib/dpkg/status'):
                self.timer_conn = self.timer.timeout.connect(make_m3u2(namex))
            else:
                self.timer.callback.append(make_m3u2(namex))
            self.timer.start(500, True)
            # make_m3u2(namex)

    def convert(self):
        # self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?")% self.name, MessageBox.TYPE_YESNO, timeout = 10, default = True)
        self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?\n\nAttention!! Wait more than 5 minutes!!! ")% self.name, MessageBox.TYPE_YESNO, timeout = 10, default = True)
        
    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        items = []
        url = self.url
        name = self.name
        namex = self.name.lower()
        namex = namex.replace(' ','-')
        namex = namex.strip()
        if os.path.exists(downloadparsa):
            xxxname = downloadparsa + namex + '_conv.m3u'
        else:
            xxxname = '/tmp/' + namex + '_conv.m3u'
        try:
            with open(xxxname, 'w') as e:
                e.write("#EXTM3U\n")
                content = getUrl('https://www.parsatv.com/m/')
                if six.PY3:
                    content = six.ensure_str(content)
                n6 = content.find("<a></a></td>")
                if str(n6) in content:
                    content.replace(str(n6),'<a></a></li></td>')
                    print('yes is n6')
                else:
                    print('no, not n6 in content!')
                s1 = name + "<a></a>"
                # s1 = name + "<a></a></li></td>"
                n1 = content.find(s1)
                n2 = content.find("<td id=", n1)
                content2 = content[n1:n2]
                print("showContent22 content2=", content2)
                #<li><a href="https://www.parsatv.com/m/name=Abadan#ostani"><button class="myButton">Abadan</button></a></li>
                #<li><a href="https://www.parsatv.com/m/name=Song-TV-Armenia#armenian"><button class="myButton">Song TV</button></a></li>
                # regexvideo = '<li><a href="(.*?)".*?"myButton">(.*?)</button></a></li>'
                regexvideo = '<li><a href="(.+?)#.*?"><button.*?myButton">(.+?)</button'
                match = re.compile(regexvideo,re.DOTALL).findall(content2)
                print("showContent22 match =", match)
                for url, name in match:
                    if url.startswith('http'):
                        url = url.replace(' ','%20')
                        name1 = name.replace('%20', ' ')
                        # print("getVideos15 name =", name1)
                        # print("getVideos15 url =", url)
                        item = name1 + "###" + url
                        items.append(item)
                        #save m3u
                        e.write('#EXTINF:-1,' + name1 +'\n')
                        e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                        e.write(url +'\n')
                        # content = getUrl(url)
                        # if six.PY3:
                            # content = six.ensure_text(content, "utf-8", "ignore")
                        # # if six.PY3:
                            # # # content = six.ensure_binary(content)
                            # # content = content.decode("utf-8")
                        # # content =convert_to_unicode(content)
                        # print("parsatv3 content B =", content)
                        # n1 = content.find('class="myButton" id=', 0)
                        # n2 = content.find("</button></a>", n1)
                        # content2 = content[n1:n2]
                        # # if six.PY3:
                            # # content2 = content2.decode("utf-8")
                        # if content2 != None:
                            # regexvideo = '<a href="(.+?)"><b'
                            # match = re.compile(regexvideo,re.DOTALL).findall(content2)
                            # print("parsatv3 match =", match)
                            # for url2 in match:
                                # if url2.startswith('http'):
                                    # url2 = url2.replace(' ','%20')
                                    # print('matchh ', url2)
                                    # e.write(url2 +'\n')

            #save m3u end
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
            # e.close()
            self['info'].setText(_('Please select ...'))
            showlistpars(self.names, self['text'])
            print('-------------parsatv-------------')

        except Exception as e:
            print('errorc ', e)

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        content = getUrl(url)
        if six.PY3:
            content = content.decode("utf-8")
        # content =convert_to_unicode(content)
        print("parsatv3 B =", content)
        n1 = content.find('class="myButton" id=', 0)
        n2 = content.find("</button></a>", n1)
        content = content[n1:n2]
        regexvideo = '<a href="(.+?)"><b'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print("getVideos parsatv3 match =", match)
        for url in match:
            url = url
            name = name
        self.session.open(Playgo, name, url)

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
        self.name = 'ParsaSport'
        # self.url = 'http://www.parsatv.com/m/name=Varzesh-TV#persian'
        self.url2 ='http://www.parsatv.com/streams/fetch/varzeshtv.php'
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
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'yellow': self.convert,
         'cancel': self.close}, -2)

    def convert2(self, result):
        if result:
            namex = self.name.lower()
            namex = namex.replace(' ','-')
            namex = namex.strip()
            if os.path.exists('/var/lib/dpkg/status'):
                self.timer_conn = self.timer.timeout.connect(make_m3u2(namex))
            else:
                self.timer.callback.append(make_m3u2(namex))
            self.timer.start(500, True)

    def convert(self):
        self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?\n\nAttention!! Wait more than 5 minutes!!! ")% self.name, MessageBox.TYPE_YESNO, timeout = 10, default = True)
        #self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?")% self.name, MessageBox.TYPE_YESNO, timeout = 10, default = True)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        items = []
        url = self.url
        namex = self.name.lower()
        namex = namex.replace(' ','-')
        namex = namex.strip()
        if os.path.exists(downloadparsa):
            xxxname = downloadparsa + namex + '_conv.m3u'
        else:
            xxxname = '/tmp/' + namex + '_conv.m3u'
        try:
            content = getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            n1 = content.find('<td id="persian">', 0)
            n2 = content.find("</ul></td>", n1)
            content = content[n1:n2]
            regexvideo = '<li><a href="(.+?)#.*?"><button.*?myButton">(.+?)</button'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print("parsasport match =", match)
            with open(xxxname, 'w') as e:
                e.write("#EXTM3U\n")
                for url, name in match:
                    if url.startswith('http'):
                        url = url.replace(' ','%20')
                        if 'sport' in str(url).lower():
                            name1 = name.replace('%20', ' ')
                            # print("getVideos15 name =", name1)
                            # print("getVideos15 url =", url)
                            item = name1 + "###" + url
                            items.append(item)
                            #save m3u
                            e.write('#EXTINF:-1,' + name1 +'\n')
                            e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                            e.write(url +'\n')
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
            # e.close()
            self['info'].setText(_('Please select ...'))
            showlistpars(self.names, self['text'])
            print('-------------sport-------------')

        except Exception as e:
            print('errorc ', e)

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        try:
            content = getUrl(url)
            if six.PY3:
                content = content.decode("utf-8")
            # content =convert_to_unicode(content)
            # print("parsasport content B =", content)
            n1 = content.find('class="myButton" id=', 0)
            n2 = content.find("</button></a>", n1)
            content = content[n1:n2]
            regexvideo = '<a href="(.+?)"><b'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            # print("parsasport match =", match)
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
        self.name = 'ParsaTv'
        self.url = 'https://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        # self['key_yellow'].hide()
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'yellow': self.convert,
         'cancel': self.close}, -2)

    def convert2(self, result):
        if result:
            namex = self.name.lower()
            namex = namex.replace(' ','-')
            namex = namex.strip()
            if os.path.exists('/var/lib/dpkg/status'):
                self.timer_conn = self.timer.timeout.connect(make_m3u2(namex))
            else:
                self.timer.callback.append(make_m3u2(namex))
            self.timer.start(500, True)

    def convert(self):
        self.session.openWithCallback(self.convert2,MessageBox,_("Do you want to Convert %s to favorite .tv ?\n\nAttention!! Wait more than 5 minutes!!! ")% self.name, MessageBox.TYPE_YESNO, timeout = 10, default = True)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        items = []
        url = self.url
        namex = self.name.lower()
        namex = namex.replace(' ','-')
        namex = namex.strip()
        if os.path.exists(downloadparsa):
            xxxname = downloadparsa + namex + '_conv.m3u'
        else:
            xxxname = '/tmp/' + namex + '_conv.m3u'
        try:
            content = getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            n1 = content.find('<td id="persian">', 0)
            n2 = content.find("</ul></td>", n1)
            content = content[n1:n2]
            regexvideo = '<li><a href="(.+?)#.*?"><button.*?myButton">(.+?)</button'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print("parsatv t match =", match)
            with open(xxxname, 'w') as e:
                e.write("#EXTM3U\n")
                for url, name in match:
                    if url.startswith('http'):
                        url = url.replace(' ','%20')
                        name1 = name.replace('%20', ' ')
                        # print("getVideos15 name =", name1)
                        # print("getVideos15 url =", url)
                        item = name1 + "###" + url
                        items.append(item)
                        #save m3u
                        e.write('#EXTINF:-1,' + name1 +'\n')
                        e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                        e.write(url +'\n')

            #save m3u end
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
            # e.close()
            self['info'].setText(_('Please select ...'))
            showlistpars(self.names, self['text'])
            print('-------------parsatv-------------')

        except Exception as e:
            print('errorc ', e)

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        try:
            content = getUrl(url)
            if six.PY3:
                content = content.decode("utf-8")
            # content =convert_to_unicode(content)
            # print("parsatv content B =", content)
            n1 = content.find('class="myButton" id=', 0)
            n2 = content.find("</button></a>", n1)
            content = content[n1:n2]
            regexvideo = '<a href="(.+?)"><b'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            # print("parsatv match =", match)
            for url in match:
                name = name
                self.session.open(Playgo, name, url)
        except:
            print('error: ')
            pass

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
        print("Here in Playgo name A =", name)
        name = name.replace(":", "-")
        name = name.replace("&", "-")
        name = name.replace(" ", "-")
        name = name.replace("/", "-")
        name = name.replace("›", "-")
        name = name.replace(",", "-")
        print("Here in Playgo name B2 =", name)
        if url is not None:
            url = str(url)
            url = url.replace(":", "%3a")
            url = url.replace("\\", "/")
            print("Playgo url final= ", url)
            ref = "4097:0:1:0:0:0:0:0:0:0:" + url
            print("Playgo ref= ", ref)
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


def make_m3u2(namex):
    if checkInternet():
        if os.path.exists(downloadparsa):
            xxxname = downloadparsa + str(namex) + '_conv.m3u'
            xxxnamex = downloadparsa + str(namex) + '.m3u'
        else:
            xxxname = '/tmp/' + str(namex) + '_conv.m3u'
            xxxnamex = '/tmp/' + str(namex) + '.m3u'
        if not os.path.exists(xxxname):
            return
        try:
            with open(xxxnamex, 'w') as e:
                e.write("#EXTM3U\n")
                file_read = open(xxxname, 'rb') #.readlines()
                file_read = [x.decode('utf8').strip() for x in file_read.readlines()]
                for line in file_read:
                    line = line.replace(' ','%20')
                    if line.startswith('#EXTINF'):
                        name = '%s' % line.split(',')[-1]
                        name = name.replace('%20', ' ').rstrip ('\n')
                        e.write('#EXTINF:-1,' + name +'\n')
                        e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
                        # continue
                    elif line.startswith("http"):
                        if six.PY3:
                            line = line.encode()

                        content = getUrl(line)
                        if six.PY3:
                            content = six.ensure_text(content, "utf-8", "ignore")
                        print("parsatv content c =", content)
                        n1 = content.find('class="myButton" id=', 0)
                        n2 = content.find("</button></a>", n1)
                        content2 = content[n1:n2]
                        if content2 != None:
                            regexvideo = '<a href="(.+?)"><b'
                            match = re.compile(regexvideo,re.DOTALL).findall(content2)
                            print("parsatv match =", match)
                            for url2 in match:
                                if url2.startswith('http'):
                                    url2 = url2.replace(' ','%20')
                                    print('matchh ', url2)
                                    e.write(url2 +'\n')
                # e.close()
            convert_bouquet(namex)
        except Exception as e:
            print('error: ', e)

def convert_bouquet(namex):
    if os.path.exists(downloadparsa):
        xxxnamex = str(downloadparsa) + str(namex) + '.m3u'
    else:
        xxxnamex = '/tmp/' + str(namex) + '.m3u'
    if not os.path.exists(xxxnamex):
        return
    name = namex.replace(' ','-').lower()
    name = namex.strip()
    parsabouquet = 'userbouquet.%s.tv' % name
    desk_tmp = ''
    in_bouquets = 0
    if os.path.isfile('/etc/enigma2/%s' % parsabouquet):
            os.remove('/etc/enigma2/%s' % parsabouquet)
    with open('/etc/enigma2/%s' % parsabouquet, 'w') as outfile:
        outfile.write('#NAME %s\r\n' % name.capitalize())
        for line in open(xxxnamex):
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
    message = (_("Bouquet successfully exported"))
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
    if not os.path.exists('/var/lib/dpkg/status'):
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

