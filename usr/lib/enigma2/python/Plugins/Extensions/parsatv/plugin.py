#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             09/02/2021               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.InfoBarGenerics import *
from Screens.InfoBar import MoviePlayer, InfoBar
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Tools.Directories import *
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, fileExists
from enigma import *
from enigma import RT_HALIGN_LEFT, getDesktop, RT_HALIGN_RIGHT, RT_HALIGN_CENTER
from enigma import eTimer, eListboxPythonMultiContent, eListbox, eConsoleAppContainer, gFont
from os import path, listdir, remove, mkdir, chmod
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import os
import re
import sys
import shutil
import ssl
import glob
from Tools.LoadPixmap import LoadPixmap
from Components.Console import Console as iConsole
global isDreamOS
global pngx, pngl, pngs
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

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse
    from urllib.parse import urlencode, quote, quote_plus
    from urllib.request import urlretrieve
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote, quote_plus
    from urllib import urlretrieve


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
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def checkStr(txt):
    if PY3:
        if type(txt) == type(bytes()):
            txt = txt.decode('utf-8')
    else:
        if type(txt) == type(unicode()):
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

def checkUrl(url):
    try:
        response = checkStr(urlopen(url, None, 5))
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
    print(" Here in getUrl url =", url)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = checkStr(urlopen(req))
    # response = checkStr(ssl_urlopen(req))    
    link = response.read()
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
currversion = '1.1'
title_plug = '..:: Parsa TV V. %s ::..' % currversion
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
skin_path = plugin_path
pluglogo = plugin_path + '/res/pics/logo.png'
pngx = plugin_path + '/res/pics/plugins.png'
pngl = plugin_path + '/res/pics/plugin.png'
pngs = plugin_path + '/res/pics/setting.png'
HD = getDesktop(0).size()


if HD.width() > 1280:
    if isDreamOS:
        skin_path = plugin_path + '/res/skins/fhd/dreamOs/'
    else:
        skin_path = plugin_path + '/res/skins/fhd/'
else:
    if isDreamOS:
        skin_path = plugin_path + '/res/skins/hd/dreamOs/'
    else:
        skin_path = plugin_path + '/res/skins/hd/'

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
        res.append(MultiContentEntryText(pos = (60, 5), size = (1000, 50), font = 1, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
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
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngx)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1200, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 6), size = (34, 25), png = loadPNG(pngx)))
        res.append(MultiContentEntryText(pos = (60, 5), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT))
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
        self.url = 'http://www.parsatv.com/streams/fetch/varzeshtv.php'
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
        url = self.url
        name = self.name
        content = getUrl(url)
        self.names = []
        self.urls = []        
        
        xxxname = '/tmp/temporary.m3u'
        if os.path.exists(xxxname):
            print('permantly remove file ', file)
            os.remove(xxxname)        
        with open(xxxname, 'w') as e:
            e.write("#EXTM3U\n")
            n1 = content.find('name="link"', 0)
            n2 = content.find("</select>", n1)
            content2 = content[n1:n2]
            # print("match content2=", content2)
            regexvideo = 'value=".*?link=(.*?)".*?>(.*?)</option>'
            match = re.compile(regexvideo,re.DOTALL).findall(content2)
            # print("match =", match)
            
            for url, name in match:   
                url = "http://www.parsatv.com/streams/fetch/varzeshtv.php?link=" + url
                name = 'Sport ' + name
                pic = " "                 
                print("getVideos5 name =", name)
                print("getVideos5 url =", url)
                name1 = name.replace("&#x27;","'").replace("&amp;","&") #url2
            
                e.write('#EXTINF:-1,' + name1 +'\n')
                e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")                    
                e.write(url+'\n')    

                self.names.append(name1)
                self.urls.append(url)

        self['info'].setText(_('Please select ...'))
        showlistpars(self.names, self['text'])


    def make_m3u(self):
        namex = self.name
        name = 'sport'
        url = ''
        xxxname2 = '/tmp/temporary2.m3u'
        if os.path.exists(xxxname2):
            print('permantly remove file ', xxxname2)
            os.remove(xxxname2)        
        xxxname = '/tmp/temporary.m3u'
        if not os.path.exists(xxxname):
            return
        with open(xxxname2, 'w') as e:
            e.write("#EXTM3U\n")
            file_read = open(xxxname).readlines() 
            for line in file_read:
                if line.startswith('#EXTINF'):
                    name = '%s' % line.split(',')[-1]            
                    name1 = name.replace('%20', ' ').rstrip ('\n')
                elif line.startswith("http"):
                    url =line
                    content = getUrl(url)
                    n1 = content.find('<body>', 0)
                    n2 = content.find("</body>", n1)
                    content = content[n1:n2]
                    regexvideo = '.*?file:.*?"(.*?)"'
                    match = re.compile(regexvideo,re.DOTALL).findall(content)
                    # print("getVideos match =", match)
                    for url in match:
                        url = url
                        # url = url.replace('https','http')
                    print("getVideos5 name =", name1)
                    print("getVideos5 url =", url)                        
                    e.write('#EXTINF:-1,' + name1 +'\n')
                    e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")                    
                    e.write(url+'\n') 
        convert_bouquet(namex)            

    def okRun(self):

        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('nameok : ', name)
        # print('urlok:  ', url)
        # try:
        content = getUrl(url)
        # print("content B =", content)
        n1 = content.find('<body>', 0)
        n2 = content.find("</body>", n1)
        content = content[n1:n2]
        regexvideo = '.*?file:.*?"(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        # print("getVideos match =", match)
        for url in match:
            # url = url.replace('https','http')
            name = name.replace('%20', ' ')
            pic = ''                 
            # print("getVideos15 name =", name)
            # print ("getVideos15 url =", url)
            self.session.open(Playgo, name, url)
        # except:
            # print('error: ')
            # pass



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
        xxxname = '/tmp/temporary.m3u'
        if os.path.exists(xxxname):
            print('permantly remove file ', xxxname)
            os.remove(xxxname)        
        with open(xxxname, 'w') as e:
            e.write("#EXTM3U\n")        

            url = self.url
            name = self.name
            content = getUrl(url)
            # try:
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
                print("getVideos15 name =", name1)
                print("getVideos15 url =", url)
                
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
        # except:
            # print('error: ')
            # pass


    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            content = getUrl(url)
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

    def make_m3u(self):
        namex = self.name
        name = 'ParsaTv'
        url = ''
        xxxname2 = '/tmp/temporary2.m3u'
        if os.path.exists(xxxname2):
            print('permantly remove file ', xxxname2)
            os.remove(xxxname2)        
        xxxname = '/tmp/temporary.m3u'
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
                    # print("content B =", content)
                    n1 = content.find('class="myButton" id=', 0)
                    n2 = content.find("</button></a>", n1)
                    content = content[n1:n2]
                    regexvideo = '<a href="(.*?)"><b'
                    match = re.compile(regexvideo,re.DOTALL).findall(content)
                    # print("getVideos match =", match)
                    for url in match:
                        url=url
                        # url = url.replace('https','http')
                    print("getVideos5 name =", name)
                    print("getVideos5 url =", url) 
                    
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
    # xxxname = '/tmp/temporary.m3u'
    xxxname = '/tmp/temporary2.m3u'
    name = namex.replace(' ','').lower() 
    if not os.path.exists(xxxname):
        self.mbox = self.session.open(openMessageBox, _('Check  /tmp/temporary2.m3u'), openMessageBox.TYPE_INFO, timeout=5)
        return        
    parsabouquet = 'userbouquet.%s.tv' % name
    # self.iConsole = iConsole()
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
    desc_plugin = (_('..:: Parsa TV by Lululla %s ::.. ' % currversion))
    name_plugin = (_('Parsa TV'))
    # main_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_MENU, fnc = StartSetup, needsRestart = True)
    extensions_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main, needsRestart = True)
    result = [PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_PLUGINMENU, icon = ico_path, fnc = main)]
    result.append(extensions_menu)
    # result.append(main_menu)
    return result
