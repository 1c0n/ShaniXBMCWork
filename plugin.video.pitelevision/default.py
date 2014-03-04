import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.dramasonline'
selfAddon = xbmcaddon.Addon(id=addon_id)
  
 
mainurl='http://www.pitelevision.com'

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def Colored(text = '', colorid = '', isBold = False):
	if colorid == 'ZM':
		color = 'FF11b500'
	elif colorid == 'EB':
		color = 'FFe37101'
	elif colorid == 'bold':
		return '[B]' + text + '[/B]'
	else:
		color = colorid
		
	if isBold == True:
		text = '[B]' + text + '[/B]'
	return '[COLOR ' + color + ']' + text + '[/COLOR]'	
	
def addDir(name,url,mode,iconimage	,showContext=False, showLiveContext=False,isItFolder=True, pageNum=""):
#	print name
#	name=name.decode('utf-8','replace')
	h = HTMLParser.HTMLParser()
	name= h.unescape(name.decode("utf8")).encode("ascii","ignore")
	#print  name
	#print url
	#print iconimage
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	if len(pageNum)>0:
		u+="&pageNumber="+pageNum
	ok=True
#	print iconimage
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DM")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
		cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
		liz.addContextMenuItems([('Play Youtube video',cmd3),('Play DailyMotion video',cmd1),('Play Tune.pk video',cmd2)])
	
	if showLiveContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "RTMP")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "HTTP")
		liz.addContextMenuItems([('Play RTMP Steam (flash)',cmd1),('Play Http Stream (ios)',cmd2)])
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok
	


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param




def Addtypes():
	#2 is series=3 are links
	addDir('Video On Demand' ,'http://www.pitelevision.com/index.php?option=com_allvideoshare&view=category&slg=on-demand&orderby=default&lang=en' ,2,'') #links 
	addDir('Live Channels' ,'http://www.pitelevision.com/index.php?option=com_allvideoshare&view=category&slg=live-channels&orderby=default&lang=en' ,3,'')
	#addDir('GeoTv Shows' ,'http://www.dramasonline.com/geo-tv-latest-dramas-episodes-online/' ,2,'')
	#addDir('AryDigital Shows' ,'http://www.dramasonline.com/ary-digital-tv-latest-dramas-episodes-online/' ,2,'')
	#addDir('Hum Sitaray Shows' ,'http://www.dramasonline.com/hum-sitaray-latest-dramas-episodes-online/' ,2,'')
	#addDir('Express Shows' ,'http://www.dramasonline.com/express-entertainment-latest-dramas-episodes-online/' ,2,'')
	#addDir('APlus Shows' ,'http://www.dramasonline.com/aplus-entertainment-latest-dramas-episodes-online/' ,2,'')
	#addDir('Teleplays' ,'http://www.dramasonline.com/?cat=255' ,3,'')# these are is links
	#addDir('Top Rated Dramas' ,'http://www.dramasonline.com/' ,5,'') # top 
	#addDir('Live Channels' ,'http://www.dramasonline.com/category/live-channels/' ,6,'') ##
	addDir('Settings' ,'http://www.dramasonline.com/category/live-channels/' ,8,'',isItFolder=False) ##
	return

def AddVOD(Fromurl):
#	print Fromurl
	print 'ere'
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	#print link
	regstring='<div class="a.*href="(.*)"\'>\s*.*<h2><span>(.*?)<.*\s*.*src="(.*?)"'
	match =re.findall(regstring, link)
	print match


	for cname in match:
		if mode==2:
			modeToUse=3; # series, 4=enteries
			if 'Music' in cname[1] or 'Films' in cname[1] or 'telefilms' in cname[1] or 'Entertainment' in cname[1]:
				modeToUse=4
		else:
			modeToUse=4;
		addDir(cname[1] ,mainurl+cname[0] ,modeToUse,cname[2])#name,url,img

	
	return

	
def ShowSettings(Fromurl):
	selfAddon.openSettings()



def AddEnteries(Fromurl):
	print Fromurl
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	print 'hre'
	match =re.findall('<div class="a.*href="(.*)"\'>\s*.*\s*.*src="(.*?)".*\s*.*?>(.*?)<', link)
	print 'match',match
	for cname in match:
		addDir(cname[2] ,mainurl+cname[0] ,5,cname[1],isItFolder=False)
		

	match =re.findall('<span class="pagenav">Next</span></li', link)
	match2 =re.findall('next', link)
	
	if len(match)==0 and len(match2)>0:
		print 'next page is not disabled',PageNumber
		url=Fromurl;
		print 'calculating pnum'
		if len(PageNumber)>0:
			print 'here'
			pNumber=str(int(PageNumber) + 16)
		else:
			print 'there'
			pNumber='16'
		print 'trying1'	
		if 'limitstart' in url:
			print 'trying2'
			url =url.split("&limitstart")[0]
		print 'trying3'
		url+="&limitstart="+pNumber
		addDir('Next Page' , url ,4,'',pageNum=pNumber)
	
	return
	
def AddChannels(liveURL):
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="videopart">\s*<div class="paneleft">\s*<a.*href="(.*?)".*title="(.*?)".*<img.*src="(.*?)"', link,re.M)

	print match
	#h = HTMLParser.HTMLParser()
	for cname in match:
		addDir(Colored(cname[1],'ZM') ,cname[0] ,7,cname[2], False, True,isItFolder=False)		#name,url,mode,icon

	return	



def PlayShowLink ( url ): 

	line1="Fetching URL";
	time=2000
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

#	url = tabURL.replace('%s',channelName);
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print url
	match= re.findall('<param name="flashvars" .*?vid=(.*?)&amp*.?pid=(.*?)"', link)
	vidId=match[0][0]
	pid=match[0][1]
	url="http://www.pitelevision.com/index.php?option=com_allvideoshare&view=config&vid=%s&pid=%s&lang=en"%(vidId,pid)
	print 'url',url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print url
	match= re.findall('<video>(.*?)<', link)
	print 'lowmatch', match
	lowLink=''
	if len(match)>0:
		lowLink=match[0]
	match= re.findall('<hd>(.*?)<', link)
	hdLink=''
	if len(match)>0:
		hdLink=match[0]
		
	print 'Low and HD Link',lowLink,hdLink
	urlToPlay=''
	if len(hdLink)>0:
		urlToPlay=hdLink
	
	if len(urlToPlay)<=0:
		urlToPlay=lowLink
	print 'heressss'
	urlToPlay=urlToPlay.replace(" ","%20")
	if 'youtube' not in urlToPlay:
		line1 = "Playing Video"
		time=2000
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(urlToPlay,listitem)
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(playlist)
	else:
		line1 = "Playing Youtube Video"
		time=2000
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		youtubecode= match =re.findall('watch\?v=(.*)', urlToPlay)
		print 'youtubecode',youtubecode
		youtubecode=youtubecode[0]
		uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
		print 'going to play',uurl;
	#	print uurl
		xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
		
		
	return
	


def PlayLiveLink ( url ): 
	progress = xbmcgui.DialogProgress()
	progress.create('Progress', 'Fetching Streaming Info')
	progress.update( 10, "", "Finding links..", "" )

	if mode==7:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match =re.findall('"http.*(ebound).*?\?site=(.*?)"',link,  re.IGNORECASE)[0]
		cName=match[1]
		progress.update( 20, "", "Finding links..", "" )

	else:
		cName=url
	#match =re.findall('"http.*(ebound).*?\?site=(.*?)"',link,  re.IGNORECASE)[0]


	
	newURL='http://www.eboundservices.com/iframe/newads/iframe.php?stream='+ cName+'&width=undefined&height=undefined&clip=' + cName
	print newURL

	
	req = urllib2.Request(newURL)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	progress.update( 50, "", "Finding links..", "" )

	
#	match =re.findall('<iframe.+src=\'(.*)\' frame',link,  re.IGNORECASE)
#	print match
#	req = urllib2.Request(match[0])
#	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
#	response = urllib2.urlopen(req)
#	link=response.read()
#	response.close()
	time = 2000  #in miliseconds
	defaultStreamType=0 #0 RTMP,1 HTTP
	defaultStreamType=selfAddon.getSetting( "DefaultStreamType" ) 
	print 'defaultStreamType',defaultStreamType
	if 1==2 and (linkType=="HTTP" or (linkType=="" and defaultStreamType=="1")): #disable http streaming for time being
#	print link
		line1 = "Playing Http Stream"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		
		match =re.findall('MM_openBrWindow\(\'(.*)\',\'ebound\'', link,  re.IGNORECASE)
			
	#	print url
	#	print match
		
		strval = match[0]
		
		#listitem = xbmcgui.ListItem(name)
		#listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		#playlist.add (strval)
		
		#xbmc.Player().play(playlist)
		listitem = xbmcgui.ListItem( label = str(cName), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=strval )
		print "playing stream name: " + str(cName) 
		listitem.setInfo( type="video", infoLabels={ "Title": cName, "Path" : strval } )
		listitem.setInfo( type="video", infoLabels={ "Title": cName, "Plot" : cName, "TVShowTitle": cName } )
		xbmc.Player(PLAYER_CORE_AUTO).play( str(strval), listitem)
	else:
		line1 = "Playing RTMP Stream"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		progress.update( 60, "", "Finding links..", "" )

		post = {'username':'hash'}
        	post = urllib.urlencode(post)
		req = urllib2.Request('http://eboundservices.com/flashplayerhash/index.php')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
		response = urllib2.urlopen(req,post)
		link=response.read()
		response.close()
		

        
		print link
		match =re.findall("=(.*)", link)

		print url
		print match

		strval = match[0]

		#listitem = xbmcgui.ListItem(name)
		#listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		#playlist.add (strval)

		playfile='rtmp://cdn.ebound.tv/tv?wmsAuthSign=/%s app=tv?wmsAuthSign=?%s swfurl=http://www.eboundservices.com/live/v6/player.swf?domain=&channel=%s&country=GB pageUrl=http://www.eboundservices.com/iframe/newads/iframe.php?stream=%s tcUrl=rtmp://cdn.ebound.tv/tv?wmsAuthSign=?%s live=true'	% (cName,strval,cName,cName,strval)
		#playfile='rtmp://cdn.ebound.tv/tv?wmsAuthSign=/humtv app=tv?wmsAuthSign=?%s swfurl=http://www.eboundservices.com/live/v6/player.swf?domain=&channel=humtv&country=GB pageUrl=http://www.eboundservices.com/iframe/newads/iframe.php?stream=humtv tcUrl=rtmp://cdn.ebound.tv/tv?wmsAuthSign=?%s live=true'	% (strval,strval)
		progress.update( 100, "", "Almost done..", "" )
		print playfile
		#xbmc.Player().play(playlist)
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
		print "playing stream name: " + str(name) 
		#listitem.setInfo( type="video", infoLabels={ "Title": name, "Path" : playfile } )
		#listitem.setInfo( type="video", infoLabels={ "Title": name, "Plot" : name, "TVShowTitle": name } )
		xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( playfile, listitem)
		#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

	return

	
#print "i am here"
params=get_params()
url=None
name=None
mode=None
linkType=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
	linkType=args.get('linkType', '')[0]
except:
	pass


PageNumber=''
try:
	PageNumber=args.get('pageNumber', '')[0]
except:
	pass

if PageNumber==None: PageNumber=""
print 	mode

try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		Addtypes()

	elif mode==2 or mode==3:
		print "AddVOD url is ",name,url
		AddVOD(url) #adds series as well as main VOD section, both are cat.

	elif mode==4:
		print " AddEnteries Play url is "+url
		AddEnteries(url)

	elif mode==5:
		print " PlayShowLink Play url is "+url
		
		PlayShowLink(url)
	elif mode==7 or mode==9:
		print "Play url is "+url,mode
		PlayLiveLink(url)
	elif mode==8:
		print "Play url is "+url,mode
		ShowSettings(url)
except:
	print 'somethingwrong'
xbmcplugin.endOfDirectory(int(sys.argv[1]))
