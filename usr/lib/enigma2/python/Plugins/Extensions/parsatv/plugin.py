#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             10/11/2021               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function
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
from Tools.Directories import SCOPE_LANGUAGE, fileExists
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
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
from Plugins.Extensions.parsatv.Utils import *

global pngs

global downloadparsa
downloadparsa = None

from six.moves.urllib.request import urlopen
from six.moves.urllib.request import Request
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.parse import quote

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

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)

# def RequestAgent():
    # RandomAgent = choice(ListAgent)
    # return RandomAgent

# def checkStr(txt):
    # if six.PY3:
        # if isinstance(txt, type(bytes())):
            # txt = txt.decode('utf-8')
    # else:
        # if isinstance(txt, type(six.text_type())):
            # txt = txt.encode('utf-8')
    # return txt

# def convert_to_unicode(text):
    # """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    # if six.PY3:
        # if isinstance(text, str):
            # return text
        # elif isinstance(text, bytes):
            # return six.ensure_text(text, "utf-8", "ignore")
        # else:
            # raise ValueError("Unsupported string type: %s" % (type(text)))
    # elif six.PY2:
        # if isinstance(text, str):
            # return six.ensure_text(text, "utf-8", "ignore")
        # elif isinstance(text, six.text_type):
            # return text
        # else:
            # raise ValueError("Unsupported string type: %s" % (type(text)))
    # else:
        # raise ValueError("Not running on Python2 or Python 3?")

# def ReadUrl(url):
    # link = []
    # url = checkStr(url)
    # print(  "Here in ReadUrl url =", url)
    # req = Request(url)
    # req.add_header('User-Agent',RequestAgent())
    # try:
        # response = urlopen(req)
        # link=response.read()
        # response.close()
        # return link
    # except:
        # import ssl
        # gcontext = ssl._create_unverified_context()
        # response = urlopen(req, context=gcontext)
        # link=response.read()
        # response.close()
        # return link

def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)
        file_write.close()

# def web_info(message):
    # try:
        # message = quote_plus(message)
        # cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' > /dev/null 2>&1 &" % message
        # # debug(cmd, "CMD -> Console -> WEBIF")
        # os.popen(cmd)
    # except:
        # print("web_info ERROR")



currversion = '1.5'
title_plug = 'Parsa TV '
desc_plugin = ('..:: Parsa TV by Lululla %s ::.. ' % currversion)
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
res_plugin_path=plugin_path + '/res/'
pngs=res_plugin_path + 'pics/setting.png'
pluglogo=res_plugin_path + 'pics/logo.png'

if isFHD():
    skin_path=res_plugin_path + 'skins/fhd/'
else:
    skin_path=res_plugin_path + 'skins/hd/'
# if os.path.exists('/var/lib/dpkg/status'):
if DreamOS():
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
        if isFHD():
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(50)

def DListEntry(name, idx):
    res = [name]
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1900, 50), font = 7, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if isFHD():
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(22)
            self.l.setFont(0, gFont('Regular', textfont))

def OneSetListEntry(name):
    res = [name]
    if isFHD():
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

        # if os.path.exists('/var/lib/dpkg/status'):
        if DreamOS():
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
            content = ReadUrl(url)
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
        # if os.path.exists('/var/lib/dpkg/status'):
        if DreamOS():
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
            # if os.path.exists('/var/lib/dpkg/status'):
            if DreamOS():
                from Tools.BoundFunction import boundFunction
                self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2,namex))
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
                content = ReadUrl('https://www.parsatv.com/m/')
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
                        # content = ReadUrl(url)
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
        content = ReadUrl(url)
        # if six.PY3:
            # content = six.ensure_str(content)
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
        # if os.path.exists('/var/lib/dpkg/status'):
        if DreamOS():
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
            # if os.path.exists('/var/lib/dpkg/status'):
            if DreamOS():
                from Tools.BoundFunction import boundFunction
                self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2,namex))
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
            content = ReadUrl(url)
            # if six.PY3:
                # content = six.ensure_str(content)
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
            content = ReadUrl(url)
            # if six.PY3:
                # content = six.ensure_str(content)
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
        # if os.path.exists('/var/lib/dpkg/status'):
        if DreamOS():
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
            # if os.path.exists('/var/lib/dpkg/status'):
            if DreamOS():
                from Tools.BoundFunction import boundFunction
                self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2,namex))
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
            content = ReadUrl(url)
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
            content = ReadUrl(url)
            # if six.PY3:
                # content = six.ensure_str(content)
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

                        content = ReadUrl(line)
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
    message = (_("Bouquet exported"))
    web_info(message)
    ReloadBouquet()

def main(session, **kwargs):
    if checkInternet():
        # try:
            # from Plugins.Extensions.parsatv.Update import upd_done
            # upd_done()
        # except:
            # pass    
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
    # if not os.path.exists('/var/lib/dpkg/status'):
    if DreamOS():
        ico_path = plugin_path + '/res/pics/logo.png'
    extensions_menu = PluginDescriptor(name = title_plug, description = desc_plugin, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main, needsRestart = True)
    result = [PluginDescriptor(name = title_plug, description = desc_plugin, where = PluginDescriptor.WHERE_PLUGINMENU, icon = ico_path, fnc = main)]
    result.append(extensions_menu)
    return result


