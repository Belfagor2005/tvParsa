#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             25/01/2022               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function
from . import _
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import *
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
# from Screens.InfoBarGenerics import *
from Screens.InfoBarGenerics import InfoBarShowHide, InfoBarSubtitleSupport, InfoBarSummarySupport, \
	InfoBarNumberZap, InfoBarMenu, InfoBarEPG, InfoBarSeek, InfoBarMoviePlayerSummarySupport, \
	InfoBarAudioSelection, InfoBarNotifications, InfoBarServiceNotifications
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import eTimer, eListboxPythonMultiContent, eListbox, eConsoleAppContainer, gFont
from enigma import eServiceReference, iPlayableService
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
try:
    from Plugins.Extensions.parsatv.Utils import *
except:
    from . import Utils
global pngs
global downloadparsa
downloadparsa = None

PY3 = sys.version_info.major >= 3
if PY3:
        import http.client
        from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
        from urllib.error import URLError, HTTPError
        from urllib.request import urlopen, Request
        from urllib.parse import urlparse
        from urllib.parse import parse_qs, urlencode
        unicode = str; unichr = chr; long = int
        PY3 = True
else:
# if os.path.exists('/usr/lib/python2.7'):
        from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
        from urllib2 import urlopen, Request, URLError, HTTPError
        from urlparse import urlparse, parse_qs
        from urllib import urlencode
        import httplib
        import six
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

global path_skin
currversion = '1.6'
title_plug = 'Parsa TV '
desc_plugin = ('..:: Parsa TV by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('parsatv'))
pluglogo = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/logo.png".format('parsatv'))
png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('parsatv'))
path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('parsatv'))
if isFHD():
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('parsatv'))
if DreamOS():
    path_skin=path_skin + 'dreamOs/'
print('parsa path_skin: ', path_skin)

Panel_Dlist = [
 ('PARSA ALL TV'),
 ('PARSA TV CATEGORY'),
 ('PARSA SPORT'),]

class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        self.l.setItemHeight(50)
        textfont = int(24)
        self.l.setFont(0, gFont('Regular', textfont))        
        if isFHD():
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))

def DListEntry(name, idx):
    res = [name]
    png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('parsatv'))
    res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))    
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(png)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1900, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res

def OneSetListEntry(name):
    res = [name]
    png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('parsatv'))
    res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(png)))
    res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))    
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(png)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1200, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
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
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainParsa')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self['text'] = OneSetList([])
        self['title'] = Label(title_plug)
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_yellow'] = Button(_(''))
        self['key_yellow'].hide()
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def closerm(self):
        deletetmp()
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
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('ParsaTV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = 'Parsa Sport'
        self.url = 'https://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button('')
        self["key_blue"] = Button('')
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
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
            content = ReadUrl2(url)
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
            print('error parsatv2', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(parsatv3, name, url)

class parsatv3(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Parsa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        self["key_blue"] = Button(_(''))
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
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
            if DreamOS():
                from Tools.BoundFunction import boundFunction
                self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2,namex))
            else:
                self.timer.callback.append(make_m3u2(namex))
            self.timer.start(500, True)
            # make_m3u2(namex)

    def convert(self):
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
                content = ReadUrl2('https://www.parsatv.com/m/')
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
            print('error ', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        content = ReadUrl2(url)
        if six.PY3:
            content = six.ensure_str(content)
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
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Parsa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = 'ParsaSport'
        self.url2 ='http://www.parsatv.com/streams/fetch/varzeshtv.php'
        self.url ='http://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        self["key_blue"] = Button(_(''))
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
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
            content = ReadUrl2(url)
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
            print('error ', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        try:
            content = ReadUrl2(url)
            if six.PY3:
                content = six.ensure_str(content)
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
        except Exception as e:
            print('error ', str(e))

class parsatv(Screen):
    def __init__(self, session):
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Parsa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = 'ParsaTv'
        self.url = 'https://www.parsatv.com/m/'
        self['text'] = OneSetList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Convert'))
        # self['key_yellow'].hide()
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self.timer = eTimer()
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
            content = ReadUrl2(url)
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
            print('error ', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        try:
            content = ReadUrl2(url)
            if six.PY3:
                content = six.ensure_str(content)
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
        except Exception as e:
            print('error ', str(e))

class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.OkPressed,
         "hide": self.hide}, 0)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def OkPressed(self):
        self.toggleShow()

    def toggleShow(self):
        if self.skipToggleShow:
            self.skipToggleShow = False
            return
        if self.__state == self.STATE_HIDDEN:
            self.show()
            self.hideTimer.stop()
        else:
            self.hide()
            self.startHideTimer()

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()
    def lockShow(self):
        try:
            self.__locked += 1
        except:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text = ""):
        print(text + " %s\n" % obj)

# class Playgo(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):
class Playgo(
    InfoBarBase,
    InfoBarMenu,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarSubtitleSupport,
    InfoBarNotifications,
    TvInfoBarShowHide,
    Screen
):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000
    def __init__(self, session, name, url):
        global SREF, streaml
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.skinName = 'MoviePlayer'
        title = name
        streaml = False

        for x in InfoBarBase, \
                InfoBarMenu, \
                InfoBarSeek, \
                InfoBarAudioSelection, \
                InfoBarSubtitleSupport, \
                InfoBarNotifications, \
                TvInfoBarShowHide:
            x.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self['actions'] = ActionMap(['MoviePlayerActions',
         'MovieSelectionActions',
         'MediaPlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'SetupActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions',
         'InfobarSeekActions'], {'leavePlayer': self.cancel,
         'epg': self.showIMDB,
         'info': self.showinfo,
         # 'info': self.cicleStreamType,
         'tv': self.cicleStreamType,
         'stop': self.leavePlayer,
         'cancel': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        # InfoBarSeek.__init__(self, ActionMap='InfobarSeekActions')
        self.service = None
        service = None
        self.url = url
        self.pcip = 'None'
        self.name = decodeHtml(name)
        self.state = self.STATE_PLAYING
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        if '8088' in str(self.url):
            # self.onLayoutFinish.append(self.slinkPlay)
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            # self.onLayoutFinish.append(self.cicleStreamType)
            self.onFirstExecBegin.append(self.cicleStreamType)
        self.onClose.append(self.cancel)

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: _('4:3 Letterbox'),
         1: _('4:3 PanScan'),
         2: _('16:9'),
         3: _('16:9 always'),
         4: _('16:10 Letterbox'),
         5: _('16:10 PanScan'),
         6: _('16:9 Letterbox')}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
         1: '4_3_panscan',
         2: '16_9',
         3: '16_9_always',
         4: '16_10_letterbox',
         5: '16_10_panscan',
         6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showinfo(self):
        debug = True
        sTitle = ''
        sServiceref = ''
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename != None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl != None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec : ' + str(sTagAudioCodec)
            self.mbox = self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        except:
            pass
        return

    def showIMDB(self):
        TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
        IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
        if os.path.exists(TMDB):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists(IMDb):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)

        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self, servicetype, url):
        name = self.name
        ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('reference:   ', ref)
        if streaml == True:
            url = 'http://127.0.0.1:8088/' + str(url)
            ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
            print('streaml reference:   ', ref)
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streml
        streaml = False
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        currentindex = 0
        streamtypelist = ["4097"]
        # if "youtube" in str(self.url):
            # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # return
        if isStreamlinkAvailable():
            streamtypelist.append("5002") #ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            streaml = True
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openTest(self.servicetype, url)
    def up(self):
        pass

    def down(self):
        self.up()

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback != None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.isfile('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(SREF)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        streaml = False
        self.close()

    def leavePlayer(self):
        self.close()

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
                    if line.startswith("http"):
                        # if six.PY3:
                            # line = line.encode()
                        # content = ReadUrl2(line)
                        # if six.PY3:
                            # content = six.ensure_text(content, "utf-8", "ignore")
                        if sys.version_info.major == 3:
                             import urllib.request as urllib2
                        elif sys.version_info.major == 2:
                             import urllib2
                        req = urllib2.Request(line)                      
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        r = urllib2.urlopen(req,None,15)
                        link = r.read()
                        r.close()
                        content = link
                        if str(type(content)).find('bytes') != -1:
                            try:
                                content = content.decode("utf-8")                
                            except Exception as e:                   
                                   print("Error: ", str(e))                               
                            
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
                e.close()
            convert_bouquet(namex)
        except Exception as e:
            print('error ', str(e))

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
    ReloadBouquets()

def checks():
    from Plugins.Extensions.parsatv.Utils import checkInternet
    checkInternet()
    chekin= False
    if checkInternet():
        chekin = True
    return chekin

def main(session, **kwargs):
    if checks:
        try:
            from Plugins.Extensions.parsatv.Update import upd_done
            upd_done()
        except:
            pass
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


