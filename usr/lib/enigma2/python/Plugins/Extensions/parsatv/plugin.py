#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             12/09/2023               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function

# Standard library
import codecs
from json import loads as json_loads
from re import compile, DOTALL, sub
from sys import version_info
from datetime import datetime
from os.path import exists, join, isfile
from os import remove, stat, system as os_system

# Third-party (Enigma2 core + Tools)
from enigma import (
	RT_VALIGN_CENTER,
	RT_HALIGN_LEFT,
	eListboxPythonMultiContent,
	eServiceReference,
	gFont,
	getDesktop,
	iPlayableService,
	loadPNG,
	eTimer
)
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import config
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryPixmapAlphaTest, MultiContentEntryText
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBarGenerics import (
	InfoBarAudioSelection,
	InfoBarMenu,
	InfoBarNotifications,
	InfoBarSeek,
	InfoBarSubtitleSupport,
)
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
import six

# Local imports (internal modules)
from . import _, paypal
from . import Utils
from . import html_conv
from .Console import Console as xConsole

global downloadparsa, path_skin, pngs

downloadparsa = None
_session = None

PY3 = version_info.major >= 3
if PY3:
	from urllib.request import urlopen, Request
	unicode = str
	unichr = chr
	long = int
else:
	from urllib2 import urlopen, Request

try:
	from Components.UsageConfig import defaultMoviePath
	downloadparsa = defaultMoviePath()
except:
	if exists("/usr/bin/apt-get"):
		downloadparsa = ('/media/hdd/movie/')
if not PY3:
	try:
		import ssl
		sslContext = ssl._create_unverified_context()
	except:
		sslContext = None
try:
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


currversion = '1.8'
title_plug = 'Parsa TV '
desc_plugin = ('..:: Parsa TV by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('parsatv'))
pluglogo = join(plugin_path, 'res/pics/logo.png')
png = join(plugin_path, 'res/pics/tv.png')
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS90dlBhcnNhL21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvdHZQYXJzYQ=='
screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
	path_skin = plugin_path + '/res/skins/uhd/'
elif screenwidth.width() == 1920:
	path_skin = plugin_path + '/res/skins/fhd/'
else:
	path_skin = plugin_path + '/res/skins/hd/'

if Utils.DreamOS():
	path_skin = path_skin + 'dreamOs/'
print('parsa path_skin: ', path_skin)
referer = 'https://www.parsatv.com/'
aspect_manager = Utils.AspectManager()

Panel_Dlist = [
	('PARSA ALL TV'),
	('PARSA TV CATEGORY'),
	('PARSA SPORT')
]


# filter list assign png
EXTRAD = "radio", "radyo", "mix", "fm", "kbit", "rap", "metal", "alternative"
EXTXXX = "adult", "xxx"
EXTCAM = "webcam", "webcams"
EXTMUS = "music", "mtv", "deluxe", "djing", "fashion", "kiss", "mpeg", "sluhay", "stingray", "techno", "viva", "country", "vevo"
EXTSPOR = "sport", "boxing", "racing", "fight", "golf", "knock", "harley", "futbool", "motor", "nba", "nfl", "bull", "poker", "billiar", "fite"
EXTRLX = "relax", "nature", "escape"
EXTMOV = "movie", "film"
EXTWEA = "weather"
EXTFAM = "family"
EXTREL = "religious"
EXTSHP = "shop"
EXTTRV = "travel"


def returnpng(name):
	if 'radio' in name.lower():
		png = join(plugin_path, 'res/pics/radio.png')
	elif 'webcam' in name.lower():
		png = join(plugin_path, 'res/pics/webcam.png')
	elif 'music' in name.lower():
		png = join(plugin_path, 'res/pics/music.png')
	elif 'sport' in name.lower():
		png = join(plugin_path, 'res/pics/sport.png')
	elif 'travel' in name.lower():
		png = join(plugin_path, 'res/pics/travel.png')
	elif 'relax' in name.lower():
		png = join(plugin_path, 'res/pics/relax.pngparsatv')
	elif 'xxx' in name.lower():
		png = join(plugin_path, 'res/pics/xxx.png')
	elif 'movie' in name.lower():
		png = join(plugin_path, 'res/pics/movie.png')
	elif 'family' in name.lower():
		png = join(plugin_path, 'res/pics/family.png')
	elif 'religious' in name.lower():
		png = join(plugin_path, 'res/pics/religious.png')
	elif 'weather' in name.lower():
		png = join(plugin_path, 'res/pics/weather.png')
	else:
		png = join(plugin_path, 'res/pics/tv.png')
	return png


class OneSetList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		if screenwidth.width() == 2560:
			self.l.setItemHeight(60)
			textfont = int(42)
			self.l.setFont(0, gFont('Regular', textfont))
		elif screenwidth.width() == 1920:
			self.l.setItemHeight(50)
			textfont = int(32)
			self.l.setFont(0, gFont('Regular', textfont))
		else:
			self.l.setItemHeight(50)
			textfont = int(24)
			self.l.setFont(0, gFont('Regular', textfont))


def OneSetListEntry(name, idx):
	res = [name]
	png = returnpng(name)
	if screenwidth.width() == 2560:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(50, 50), png=loadPNG(png)))
		res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
	elif screenwidth.width() == 1920:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 7), size=(40, 40), png=loadPNG(png)))
		res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
	else:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 10), size=(40, 40), png=loadPNG(png)))
		res.append(MultiContentEntryText(pos=(50, 0), size=(500, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
	return res


def showlistpars(data, list):
	icount = 0
	plist = []
	for line in data:
		name = data[icount]
		plist.append(OneSetListEntry(name, icount))
		icount += 1
		list.setList(plist)


def returnIMDB(text_clear):
	text = html_conv.html_unescape(text_clear)

	if Utils.is_TMDB and Utils.TMDB:
		try:
			_session.open(Utils.TMDB.tmdbScreen, text, 0)
		except Exception as e:
			print("[XCF] TMDB error:", str(e))
		return True

	elif Utils.is_tmdb and Utils.tmdb:
		try:
			_session.open(Utils.tmdb.tmdbScreen, text, 0)
		except Exception as e:
			print("[XCF] tmdb error:", str(e))
		return True

	elif Utils.is_imdb and Utils.imdb:
		try:
			Utils.imdb(_session, text)
		except Exception as e:
			print("[XCF] IMDb error:", str(e))
		return True

	_session.open(MessageBox, text, MessageBox.TYPE_INFO)
	return True


class MainParsa(Screen):
	def __init__(self, session):
		self.session = session
		global _session
		_session = session
		skin = join(path_skin, 'settings.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		self.setup_title = ('MainParsa')
		Screen.__init__(self, session)
		self.setTitle(title_plug)
		self['text'] = OneSetList([])
		self['title'] = Label(title_plug)
		self['info'] = Label(_('Loading data... Please wait'))
		self["paypal"] = Label()
		self['key_yellow'] = Button(_('Update'))
		self['key_yellow'].hide()
		self['key_green'] = Button(_('Select'))
		self['key_red'] = Button(_('Exit'))
		self["key_blue"] = Button()
		self['key_blue'].hide()
		self["key_green"].hide()
		self.Update = False
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"HotkeyActions",
				"InfobarEPGActions",
				"ChannelSelectBaseActions",
				"DirectionActions"
			],
			{
				"yellow": self.update_me,               # update_me
				"yellow_long": self.update_dev,
				"info_long": self.update_dev,
				"infolong": self.update_dev,
				"showEventInfoPlugin": self.update_dev,
				"ok": self.okRun,
				"green": self.okRun,
				"cancel": self.closerm,
				"red": self.closerm
			},
			-1
		)

		self.timer = eTimer()
		if exists('/var/lib/dpkg/status'):
			self.timer_conn = self.timer.timeout.connect(self.check_vers)
		else:
			self.timer.callback.append(self.check_vers)
		self.timer.start(500, 1)
		self.onLayoutFinish.append(self.updateMenuList)
		self.onLayoutFinish.append(self.layoutFinished)

	def check_vers(self):
		remote_version = '0.0'
		remote_changelog = ''
		req = Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
		page = Utils.urlopen(req).read()
		if PY3:
			data = page.decode("utf-8")
		else:
			data = page.encode("utf-8")
		if data:
			lines = data.split("\n")
			for line in lines:
				if line.startswith("version"):
					remote_version = line.split("=")
					remote_version = line.split("'")[1]
				if line.startswith("changelog"):
					remote_changelog = line.split("=")
					remote_changelog = line.split("'")[1]
					break
		self.new_version = remote_version
		self.new_changelog = remote_changelog
		if currversion < remote_version:
			self.Update = True
			self['key_yellow'].show()
			# self['key_green'].show()
			self.session.open(
				MessageBox,
				_(
					"New version %s is available\n\n"
					"Changelog: %s\n\n"
					"Press info_long or yellow_long button to start force updating."
				) % (self.new_version, self.new_changelog),
				MessageBox.TYPE_INFO,
				timeout=5
			)
		# self.update_me()

	def update_me(self):
		if self.Update is True:
			self.session.openWithCallback(
				self.install_update,
				MessageBox,
				_(
					"New version %s is available.\n\n"
					"Changelog: %s\n\n"
					"Do you want to install it now?"
				) % (self.new_version, self.new_changelog),
				MessageBox.TYPE_YESNO
			)
		else:
			self.session.open(
				MessageBox,
				_("Congrats! You already have the latest version..."),
				MessageBox.TYPE_INFO,
				timeout=4
			)

	def update_dev(self):
		try:
			req = Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
			page = Utils.urlopen(req).read()
			data = json_loads(page)
			remote_date = data['pushed_at']
			strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
			remote_date = strp_remote_date.strftime('%Y-%m-%d')
			self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
		except Exception as e:
			print('error xcons:', e)

	def install_update(self, answer=False):
		if answer:
			cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
			self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
		else:
			self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

	def myCallback(self, result=None):
		print('result:', result)
		return

	def layoutFinished(self):
		payp = paypal()
		self["paypal"].setText(payp)
		self.setTitle(self.setup_title)

	def closerm(self):
		Utils.deletetmp()
		self.close()

	def updateMenuList(self):
		self.menu_list = []
		for x in self.menu_list:
			del self.menu_list[0]
		list = []
		idx = 0
		for x in Panel_Dlist:
			list.append(OneSetListEntry(x, idx))
			self.menu_list.append(x)
			idx += 1
		self['text'].setList(list)
		self["key_green"].show()
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
		global _session
		_session = session
		skin = join(path_skin, 'settings.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		self.setup_title = ('ParsaTV')
		Screen.__init__(self, session)
		self.setTitle(title_plug)
		self.list = []
		self.name = 'Parsa Category'
		self.url = 'https://www.parsatv.com/m/'
		self['title'] = Label(title_plug)
		self['text'] = OneSetList([])
		self['info'] = Label(_('Loading data... Please wait'))
		self["paypal"] = Label()
		self['key_green'] = Button(_('Select'))
		self['key_red'] = Button(_('Back'))
		self['key_yellow'] = Button('')
		self["key_blue"] = Button('')
		self["key_green"].hide()
		self['key_blue'].hide()
		self.timer = eTimer()
		if Utils.DreamOS():
			self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
		else:
			self.timer.callback.append(self._gotPageLoad)
		self.timer.start(1500, True)
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"ColorActions",
				"ButtonSetupActions",
				"DirectionActions"
			],
			{
				"ok": self.okRun,
				"green": self.okRun,
				"red": self.close,
				# "yellow": self.convert,
				"cancel": self.close
			},
			-2
		)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		payp = paypal()
		self["paypal"].setText(payp)
		self.setTitle(self.setup_title)

	def _gotPageLoad(self):
		url = self.url
		name = self.name
		self.names = []
		self.urls = []
		items = []
		try:
			content = Utils.ReadUrl2(url, referer)
			if six.PY3:
				content = six.ensure_str(content)

			n6 = content.find("<a></a></td>")
			if str(n6) in content:
				content = content.replace("<a></a></td>", "<a></a></li></td>")
				print("yes is n6")
			else:
				print("no, no n6 in parsatv2!")

			regexvideo = '<tr>.*?<td id=".*?><li>(.+?)<a>.*?</td>.*?</tr>'
			match = compile(regexvideo, DOTALL).findall(content)
			for name in match:
				url = url.replace(' ', '%20')
				item = name + "###" + url + '\n'
				items.append(item)

			items.sort()
			for item in items:
				name = item.split("###")[0]
				url = item.split("###")[1]
				self.names.append(name)
				self.urls.append(url)

			self['info'].setText(_('Please select ...'))
			self["key_green"].show()
			showlistpars(self.names, self['text'])
		except Exception as e:
			print("error parsatv2", str(e))

	def okRun(self):
		if not self.names:
			return

		idx = self["text"].getSelectionIndex()

		if idx < 0 or idx >= len(self.names):
			return

		name = self.names[idx]
		url = self.urls[idx]
		self.session.open(parsatv3, name, url)


class parsatv3(Screen):
	def __init__(self, session, name, url):
		self.session = session
		global _session
		_session = session
		skin = join(path_skin, 'settings.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		self.setup_title = ('Parsa Category')
		Screen.__init__(self, session)
		self.setTitle(title_plug)
		self.list = []
		self.name = name
		self.url = url
		self['title'] = Label(title_plug)
		self['text'] = OneSetList([])
		self['info'] = Label(_('Loading data... Please wait'))
		self["paypal"] = Label()
		self['key_red'] = Button(_('Back'))
		self['key_green'] = Button(_('Play'))
		self['key_yellow'] = Button(_('Convert'))
		self["key_blue"] = Button()
		self["key_green"].hide()
		self['key_yellow'].hide()
		self['key_blue'].hide()
		self.timer = eTimer()
		if Utils.DreamOS():
			self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
		else:
			self.timer.callback.append(self._gotPageLoad)
		self.timer.start(1500, True)
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"ColorActions",
				"ButtonSetupActions",
				"DirectionActions"
			],
			{
				"ok": self.okRun,
				"green": self.okRun,
				"red": self.close,
				"yellow": self.convert,
				"cancel": self.close
			},
			-2
		)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		payp = paypal()
		self["paypal"].setText(payp)
		self.setTitle(self.setup_title)

	def convert(self, answer=None):
		if answer is None:
			self.session.openWithCallback(
				self.convert,
				MessageBox,
				_(
					"Do you want to Convert %s to favorite .tv?\n\n"
					"Attention!! It may take some time depending\n"
					"on the number of streams contained!!!"
				)
			)
		elif answer:
			namex = self.name.lower()
			namex = namex.replace(' ', '-').strip()
			if Utils.DreamOS():
				from Tools.BoundFunction import boundFunction
				self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2, namex))
			else:
				self.timer.callback.append(make_m3u2(namex))
			self.timer.start(500, True)

	def _gotPageLoad(self):
		self.names = []
		self.urls = []
		items = []

		url = self.url
		name = self.name
		namex = name.lower().replace(" ", "-").strip()

		if exists(downloadparsa):
			xxxname = downloadparsa + namex + "_conv.m3u"
		else:
			xxxname = "/tmp/" + namex + "_conv.m3u"

		try:
			with open(xxxname, "w") as e:
				e.write("#EXTM3U\n")

				content = Utils.ReadUrl2("https://www.parsatv.com/m/", referer)
				if six.PY3:
					content = six.ensure_str(content)

				if "<a></a></td>" in content:
					content = content.replace("<a></a></td>", "<a></a></li></td>")
					print("yes is n6")
				else:
					print("no, not n6 in content!")

				s1 = name + "<a></a>"
				n1 = content.find(s1)
				n2 = content.find("<td id=", n1)
				content2 = content[n1:n2]

				regexvideo = '<li><a href="(.+?)#.*?"><button.*?myButton">(.+?)</button'
				match = compile(regexvideo, DOTALL).findall(content2)

				for url, name in match:
					if url.startswith("http"):
						url = url.replace(" ", "%20")
						name1 = name.replace("%20", " ")
						item = name1 + "###" + url + "\n"
						items.append(item)

						# Write m3u
						e.write("#EXTINF:-1," + name1 + "\n")
						e.write(url + "\n")

			items.sort()
			for item in items:
				name = item.split("###")[0]
				url = item.split("###")[1]
				self.names.append(name)
				self.urls.append(url)

			self["info"].setText(_("Please select ..."))
			self["key_green"].show()
			self["key_yellow"].show()
			showlistpars(self.names, self["text"])

			print("-------------parsatv-------------")
		except Exception as e:
			print("error", str(e))

	def okRun(self):
		i = len(self.names)
		if i < 1:
			return

		idx = self["text"].getSelectionIndex()
		name = self.names[idx]
		url = self.urls[idx]

		content = Utils.ReadUrl2(url, referer)
		if six.PY3:
			content = six.ensure_str(content)

		n1 = content.find('class="myButton" id=', 0)
		n2 = content.find("</button></a>", n1)
		content = content[n1:n2]

		regexvideo = '<a href="(.+?)"><b'
		match = compile(regexvideo, DOTALL).findall(content)

		for url in match:
			pass  # last url remains (if multiple links)

		self.session.open(Playgo, name, url)


class parsasport(Screen):
	def __init__(self, session):
		self.session = session
		skin = join(path_skin, 'settings.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		self.setup_title = ('Parsa Sport')
		Screen.__init__(self, session)
		self.setTitle(title_plug)
		self.list = []
		self.name = 'ParsaSport'
		self.url2 = 'http://www.parsatv.com/streams/fetch/varzeshtv.php'
		self.url3 = 'http://www.parsatv.com/m/name=Varzesh-3'
		self.url = 'http://www.parsatv.com/m/'
		self['text'] = OneSetList([])
		self['info'] = Label(_('Loading data... Please wait'))
		self["paypal"] = Label()
		self['key_red'] = Button(_('Back'))
		self['key_green'] = Button(_('Play'))
		self['key_yellow'] = Button(_('Convert'))
		self["key_blue"] = Button()
		self["key_green"].hide()
		self['key_yellow'].hide()
		self['key_blue'].hide()
		self.timer = eTimer()
		if Utils.DreamOS():
			self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
		else:
			self.timer.callback.append(self._gotPageLoad)
		self.timer.start(1500, True)
		self['title'] = Label(title_plug)
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"ColorActions",
				"ButtonSetupActions",
				"DirectionActions"
			],
			{
				"ok": self.okRun,
				"green": self.okRun,
				"red": self.close,
				"yellow": self.convert,
				"cancel": self.close
			},
			-2
		)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		payp = paypal()
		self["paypal"].setText(payp)
		self.setTitle(self.setup_title)

	def convert(self, answer=None):
		if answer is None:
			self.session.openWithCallback(
				self.convert,
				MessageBox,
				_(
					"Do you want to Convert to favorite .tv?\n\n"
					"Attention!! It may take some time depending\n"
					"on the number of streams contained!!!"
				)
			)
		elif answer:
			namex = self.name.lower()
			namex = namex.replace(' ', '-').strip()
			if Utils.DreamOS():
				from Tools.BoundFunction import boundFunction
				self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2, namex))
			else:
				self.timer.callback.append(make_m3u2(namex))
			self.timer.start(500, True)

	def _gotPageLoad(self):
		self.names = []
		self.urls = []
		items = []

		url = self.url
		namex = self.name.lower().replace(' ', '-').strip()

		if exists(downloadparsa):
			xxxname = downloadparsa + namex + '_conv.m3u'
		else:
			xxxname = '/tmp/' + namex + '_conv.m3u'

		try:
			content = Utils.ReadUrl2(url, referer)
			if six.PY3:
				content = six.ensure_str(content)

			n1 = content.find('<td id="persian">', 0)
			n2 = content.find("</ul></td>", n1)
			content = content[n1:n2]

			regexvideo = '<li><a href="(.+?)#.*?"><button.*?myButton">(.+?)</button'
			match = compile(regexvideo, DOTALL).findall(content)

			with open(xxxname, 'w') as e:
				e.write("#EXTM3U\n")
				for url, name in match:
					if url.startswith('http') and 'sport' in url.lower():
						url = url.replace(' ', '%20')
						name1 = name.replace('%20', ' ')
						item = name1 + "###" + url + '\n'
						items.append(item)
						# Write to m3u
						e.write('#EXTINF:-1,' + name1 + '\n')
						e.write(url + '\n')

			items.sort()
			for item in items:
				name = item.split("###")[0]
				url = item.split("###")[1]
				self.names.append(name)
				self.urls.append(url)

			self['info'].setText(_('Please select ...'))
			self["key_green"].show()
			self['key_yellow'].show()
			showlistpars(self.names, self['text'])

			print('-------------sport-------------')

		except Exception as e:
			print('error', str(e))

	def okRun(self):
		i = len(self.names)
		if i < 1:
			return

		idx = self["text"].getSelectionIndex()
		name = self.names[idx]
		url = self.urls[idx]

		try:
			content = Utils.ReadUrl2(url, referer)
			if six.PY3:
				content = six.ensure_str(content)

			n1 = content.find('class="myButton" id=', 0)
			n2 = content.find("</button></a>", n1)
			content = content[n1:n2]

			regexvideo = '<a href="(.+?)"><b'
			match = compile(regexvideo, DOTALL).findall(content)

			for final_url in match:
				self.session.open(Playgo, name, final_url)

		except Exception as e:
			print('error', str(e))


class parsatv(Screen):
	def __init__(self, session):
		self.session = session
		skin = join(path_skin, 'settings.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		self.setup_title = ('Parsa TV')
		Screen.__init__(self, session)
		self.setTitle(title_plug)
		self.list = []
		self.name = 'ParsaTv'
		self.url = 'https://www.parsatv.com/m/'
		self['text'] = OneSetList([])
		self['info'] = Label(_('Loading data... Please wait'))
		self["paypal"] = Label()
		self['key_red'] = Button(_('Back'))
		self['key_green'] = Button(_('Play'))
		self['key_yellow'] = Button(_('Convert'))
		self["key_blue"] = Button()
		self["key_green"].hide()
		self['key_yellow'].hide()
		self['key_blue'].hide()
		self.timer = eTimer()
		if Utils.DreamOS():
			self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
		else:
			self.timer.callback.append(self._gotPageLoad)
		self.timer.start(1500, True)
		self['title'] = Label(title_plug)
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"ColorActions",
				"ButtonSetupActions",
				"DirectionActions"
			],
			{
				"ok": self.okRun,
				"green": self.okRun,
				"red": self.close,
				"yellow": self.convert,
				"cancel": self.close
			},
			-2
		)
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		payp = paypal()
		self["paypal"].setText(payp)
		self.setTitle(self.setup_title)

	def convert(self, answer=None):
		if answer is None:
			self.session.openWithCallback(
				self.convert,
				MessageBox,
				_(
					"Do you want to Convert to favorite .tv?\n\n"
					"Attention!! It may take some time depending\n"
					"on the number of streams contained!!!"
				)
			)
		elif answer:
			namex = self.name.lower()
			namex = namex.replace(' ', '-').strip()
			if Utils.DreamOS():
				from Tools.BoundFunction import boundFunction
				self.timer_conn = self.timer.timeout.connect(boundFunction(make_m3u2, namex))
			else:
				self.timer.callback.append(make_m3u2(namex))
			self.timer.start(500, True)

	def _gotPageLoad(self):
		self.names = []
		self.urls = []
		items = []
		url = self.url
		namex = self.name.lower().replace(' ', '-').strip()

		if exists(downloadparsa):
			xxxname = downloadparsa + namex + '_conv.m3u'
		else:
			xxxname = '/tmp/' + namex + '_conv.m3u'

		try:
			content = Utils.ReadUrl2(url, referer)
			if six.PY3:
				content = six.ensure_str(content)

			n1 = content.find('<td id="persian">', 0)
			n2 = content.find("</ul></td>", n1)
			content = content[n1:n2]

			regexvideo = '<li><a href="(.+?)#.*?"><button.*?myButton">(.+?)</button'
			match = compile(regexvideo, DOTALL).findall(content)

			with open(xxxname, 'w') as e:
				e.write("#EXTM3U\n")
				for url_item, name_item in match:
					if url_item.startswith('http'):
						url_fixed = url_item.replace(' ', '%20')
						name_fixed = name_item.replace('%20', ' ')
						item = name_fixed + "###" + url_fixed + '\n'
						items.append(item)
						# save m3u entries
						e.write('#EXTINF:-1,' + name_fixed + '\n')
						# e.write("#EXTVLCOPT:http-user-agent=fake_UA\n")
						e.write(url_fixed + '\n')

			items.sort()
			for item in items:
				name_split = item.split("###")[0]
				url_split = item.split("###")[1]
				self.names.append(name_split)
				self.urls.append(url_split)

			self['info'].setText(_('Please select ...'))
			self["key_green"].show()
			self['key_yellow'].show()
			showlistpars(self.names, self['text'])
			print('-------------parsatv-------------')

		except Exception as e:
			print('error', str(e))

	def okRun(self):
		if len(self.names) < 1:
			return

		idx = self["text"].getSelectionIndex()
		name = self.names[idx]
		url = self.urls[idx]

		try:
			content = Utils.ReadUrl2(url, referer)
			if six.PY3:
				content = six.ensure_str(content)

			n1 = content.find('class="myButton" id=', 0)
			n2 = content.find("</button></a>", n1)
			content = content[n1:n2]

			regexvideo = '<a href="(.+?)"><b'
			match = compile(regexvideo, DOTALL).findall(content)

			for video_url in match:
				self.session.open(Playgo, name, video_url)

		except Exception as e:
			print('error', str(e))


class TvInfoBarShowHide():
	""" InfoBar show/hide control, accepts toggleShow and hide actions, might start
	fancy animations. """
	STATE_HIDDEN = 0
	STATE_HIDING = 1
	STATE_SHOWING = 2
	STATE_SHOWN = 3
	skipToggleShow = False

	def __init__(self):
		self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.OkPressed, "hide": self.hide}, 0)
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

	def debug(obj, text=""):
		print(text + " %s\n" % obj)


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
		self.skinName = 'MoviePlayer'
		streaml = False
		self.allowPiP = False
		# InfoBarSeek.__init__(self, ActionMap='InfobarSeekActions')
		self.service = None
		self.url = url
		self.pcip = 'None'
		self.name = html_conv.html_unescape(name)
		self.state = self.STATE_PLAYING
		for x in (
			InfoBarBase,
			InfoBarMenu,
			InfoBarSeek,
			InfoBarAudioSelection,
			InfoBarSubtitleSupport,
			InfoBarNotifications,
			TvInfoBarShowHide
		):
			x.__init__(self)

		SREF = self.session.nav.getCurrentlyPlayingServiceReference()
		self["actions"] = ActionMap(
			[
				"MoviePlayerActions",
				"MovieSelectionActions",
				"MediaPlayerActions",
				"EPGSelectActions",
				"MediaPlayerSeekActions",
				"ColorActions",
				"OkCancelActions",
				"InfobarShowHideActions",
				"InfobarActions",
				"InfobarSeekActions"
			],
			{
				"leavePlayer": self.cancel,
				"epg": self.showIMDB,
				"info": self.showIMDB,
				# "info": self.cicleStreamType,
				"tv": self.cicleStreamType,
				"stop": self.leavePlayer,
				"cancel": self.cancel,
				"exit": self.leavePlayer,
				# "down": self.av,
				"back": self.cancel
			},
			-1
		)

		if '8088' in str(self.url):
			# self.onLayoutFinish.append(self.slinkPlay)
			self.onFirstExecBegin.append(self.slinkPlay)
		else:
			# self.onLayoutFinish.append(self.cicleStreamType)
			self.onFirstExecBegin.append(self.cicleStreamType)
		self.onClose.append(self.cancel)

	def showIMDB(self):
		text_clear = self.name
		if returnIMDB(text_clear):
			print('show imdb/tmdb')

	def slinkPlay(self, url):
		name = self.name
		ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
		print('final reference:   ', ref)
		sref = eServiceReference(ref)
		sref.setName(str(name))
		self.session.nav.stopService()
		self.session.nav.playService(sref)

	def openTest(self, servicetype, url):
		name = self.name
		ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
		print('reference:   ', ref)
		if streaml is True:
			url = 'http://127.0.0.1:8088/' + str(url)
			ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
			print('streaml reference:   ', ref)
		print('final reference:   ', ref)
		sref = eServiceReference(ref)
		sref.setName(str(name))
		self.session.nav.stopService()
		self.session.nav.playService(sref)

	def cicleStreamType(self):
		from itertools import cycle, islice
		self.servicetype = '4097'
		print('servicetype1: ', self.servicetype)
		url = str(self.url)
		streamtypelist = ["4097"]
		"""
		# if str(splitext(url)[-1]) == ".m3u8":
			# if self.servicetype == "1":
				# self.servicetype = "4097"
		# if "youtube" in str(self.url):
			# self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
			# return
		# if Utils.isStreamlinkAvailable():
			# streamtypelist.append("5002")  # ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
			# streaml = True
		# if exists("/usr/bin/gstplayer"):
			# streamtypelist.append("5001")
		# if exists("/usr/bin/exteplayer3"):
			# streamtypelist.append("5002")
		"""
		if exists("/usr/bin/apt-get"):
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
		self.cancel()

	def __evEOF(self):
		self.end = True

	def showVideoInfo(self):
		if self.shown:
			self.hideInfobar()
		if self.infoCallback is not None:
			self.infoCallback()
		return

	def showAfterSeek(self):
		if isinstance(self, TvInfoBarShowHide):
			self.doShow()

	def cancel(self):
		if isfile('/tmp/hls.avi'):
			remove('/tmp/hls.avi')
		self.session.nav.stopService()
		self.session.nav.playService(SREF)
		aspect_manager.restore_aspect
		self.close()

	def leavePlayer(self):
		self.cancel()


def make_m3u2(namex):
	if not Utils.checkInternet():
		return

	if exists(downloadparsa):
		xxxname = downloadparsa + str(namex) + '_conv.m3u'
		xxxnamex = downloadparsa + str(namex) + '.m3u'
	else:
		xxxname = '/tmp/' + str(namex) + '_conv.m3u'
		xxxnamex = '/tmp/' + str(namex) + '.m3u'

	if not exists(xxxname):
		return

	try:
		with open(xxxnamex, 'w') as e:
			e.write("#EXTM3U\n")

			with open(xxxname, 'rb') as file_read:
				lines = [x.decode('utf8').strip() for x in file_read.readlines()]

			for line in lines:
				line = line.replace(' ', '%20')

				if line.startswith('#EXTINF'):
					name = line.split(',')[-1].replace('%20', ' ').rstrip('\n')
					e.write('#EXTINF:-1,' + name + '\n')

				elif line.startswith("http"):
					req = Request(line)
					req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')

					r = urlopen(req, None, 15)
					content = r.read()
					r.close()

					if isinstance(content, bytes):
						try:
							content = content.decode("utf-8")
						except Exception as e:
							print("Error decoding content: ", str(e))

					n1 = content.find('class="myButton" id=')
					n2 = content.find("</button></a>", n1)
					content2 = content[n1:n2] if n1 != -1 and n2 != -1 else ''

					if content2:
						regexvideo = '<a href="(.+?)"><b'
						match = compile(regexvideo, DOTALL).findall(content2)

						for url2 in match:
							if url2.startswith('http'):
								url2 = url2.replace(' ', '%20')
								e.write(url2 + '\n')

		convert_bouquet(namex)

	except Exception as e:
		print('error ', str(e))


def convert_bouquet(namex):
	type = "tv"
	if "radio" in namex.lower():
		type = "radio"

	name_file = namex.replace("/", "_").replace(",", "").replace(" ", "-")
	cleanName = sub(r'[\<\>\:\"\/\\\|\?\*]', "_", str(name_file))
	cleanName = sub(r" ", "_", cleanName)
	cleanName = sub(r"\d+:\d+:[\d.]+", "_", cleanName)
	name_file = sub(r"_+", "_", cleanName)
	bouquetname = "userbouquet.%s.%s" % (name_file.lower(), type.lower())

	print("Converting Bouquet %s" % name_file)

	if exists(downloadparsa):
		file = str(downloadparsa) + str(namex) + ".m3u"
	else:
		file = "/tmp/" + str(namex) + ".m3u"

	if not exists(file):
		return

	path1 = "/etc/enigma2/" + str(bouquetname)
	path2 = "/etc/enigma2/bouquets." + str(type.lower())

	if exists(file) and stat(file).st_size > 0:
		tmplist = []
		tmplist.append("#NAME %s (%s)" % (name_file.upper(), type.upper()))
		tmplist.append("#SERVICE 1:64:0:0:0:0:0:0:0:0::%s CHANNELS" % name_file)
		tmplist.append("#DESCRIPTION --- %s ---" % name_file)

		namel = ""
		servicez = ""
		descriptionz = ""

		for line in open(file):
			if line.startswith("#EXTINF"):
				namel = "%s" % line.split(",")[-1]
				descriptiona = ("#DESCRIPTION %s" % namel).splitlines()
				descriptionz = "".join(descriptiona)

			elif line.startswith("http"):
				tag = "1"
				if type.upper() == "RADIO":
					tag = "2"

				servicea = "#SERVICE 4097:0:%s:0:0:0:0:0:0:0:%s" % (tag, line.replace(":", "%3a"))
				servicez = (servicea + ":" + namel).splitlines()
				servicez = "".join(servicez)

			if servicez not in tmplist:
				tmplist.append(servicez)
				tmplist.append(descriptionz)

		# Write bouquet file
		with open(path1, "w+") as f:
			# Read file content once to check duplicates
			f_content = f.read()
			for item in tmplist:
				if item not in f_content:
					f.write("%s\n" % item)
					print("item  -------- ", item)

		# Check if bouquet is already in bouquets file
		in_bouquets = 0
		with open("/etc/enigma2/bouquets.%s" % type.lower()) as f:
			for line in f:
				if bouquetname in line:
					in_bouquets = 1
					break

		# Append bouquet to bouquets file if not present
		if in_bouquets == 0:
			with open(path2, "a+") as f:
				bouquetTvString = "#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET \"" + str(bouquetname) + "\" ORDER BY bouquet\n"
				f.write(bouquetTvString)

		# Reload bouquets and servicelist
		try:
			from enigma import eDVBDB
			eDVBDB.getInstance().reloadServicelist()
			eDVBDB.getInstance().reloadBouquets()
			print("all bouquets reloaded...")
		except:
			os_system("wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &")
			print("bouquets reloaded...")

		_session.open(MessageBox, _("bouquets reloaded.."), MessageBox.TYPE_INFO, timeout=5)


def main(session, **kwargs):
	try:
		session.open(MainParsa)
	except:
		import traceback
		traceback.print_exc()
		pass


def Plugins(**kwargs):
	ico_path = "logo.png"
	if not exists("/var/lib/dpkg/status"):
		ico_path = plugin_path + "/res/pics/logo.png"
	extensions_menu = PluginDescriptor(
		name=title_plug,
		description=desc_plugin,
		where=PluginDescriptor.WHERE_EXTENSIONSMENU,
		fnc=main,
		needsRestart=True
	)
	result = [
		PluginDescriptor(
			name=title_plug,
			description=desc_plugin,
			where=PluginDescriptor.WHERE_PLUGINMENU,
			icon=ico_path,
			fnc=main
		)
	]
	result.append(extensions_menu)
	return result
