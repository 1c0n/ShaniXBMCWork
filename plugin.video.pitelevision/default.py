import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver
import urlparse
import HTMLParser
import xbmcaddon
from dirCreator import parseList;
from urlLib import getURL;

from operator import itemgetter
import traceback


REMOTE_DBG=False;
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)  


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


__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.dramasonline'
selfAddon = xbmcaddon.Addon(id=addon_id)
  
 
mainurl='http://www.pitelevision.com'



def Addtypes():
    parseList(getMainMenu());#caching here
    return

def getMainMenu():
    list=[]
    list.append({'name':'Video On Demand','url':'http://www.pitelevision.com/index.php?option=com_allvideoshare&view=category&slg=on-demand&orderby=default&lang=en','mode':'VOD'})
    list.append({'name':'All Live Channels','url':'http://www.pitelevision.com/index.php?option=com_allvideoshare&view=category&slg=all-channels&orderby=default&Itemid=142&lang=en','mode':'ALLC'})
    list.append({'name':'Settings','url':'Settings','mode':'Settings'})
    #print list;
    return list;

def AddVOD(Fromurl,mode):
    parseList(getVODList(Fromurl,mode));#caching here

def getVODList(Fromurl,mode):

    link=getURL(Fromurl).result
    regstring='<div class="a.*href="(.*)"\'>\s*.*<h2><span>(.*?)<.*\s*.*src="(.*?)"'
    match =re.findall(regstring, link)
    #print match
    
    listToReturn=[]
    for cname in match:
        if mode=='VOD':
            modeToUse='VODSerial'; # series, 4=enteries
            if 'Music' in cname[1] or 'Films' in cname[1] or 'Telefilms' in cname[1] or 'Entertainment' in cname[1]:
                modeToUse='VODEntry'
        else:
            modeToUse='VODEntry';
        #print modeToUse,cname[1]
        listToReturn.append({'name':cname[1],'url':mainurl+cname[0],'mode':modeToUse,'iconimage':cname[2].replace(' ','%20')})
    return listToReturn;

	
def ShowSettings(Fromurl):
	selfAddon.openSettings()


def AddEnteries(Fromurl,PageNumber,mode):
    parseList(getEnteriesList(Fromurl,PageNumber,mode));#caching here
    
def getEnteriesList(Fromurl,PageNumber,mode):
    link=getURL(Fromurl).result;
    #print 'getEnteriesList',link
    match =re.findall('<div class="a.*href="(.*)"\'>\s*.*\s*.*src="(.*?)".*\s*.*?>(.*?)<', link)
    #print 'match',match
    listToReturn=[]
    rmode='PlayVOD';
    if mode=='ALLC':
        rmode='PlayLive'
    for cname in match:
        #addDir(cname[2] ,mainurl+cname[0] ,5,cname[1],isItFolder=False)
        imageurl=cname[1].replace(' ','%20');
        url=cname[0];
        
        if not imageurl.startswith('http'): imageurl=mainurl+'/'+imageurl
        if not url.startswith('http'): url=mainurl+url
        #print imageurl    
        listToReturn.append({'name':cname[2],'url':url,'mode':rmode,'iconimage':imageurl,'isFolder':False})

    match =re.findall('<span class="pagenav">Next</span></li', link)
    match2 =re.findall('next', link)
    if len(match)==0 and len(match2)>0:
        url=Fromurl;
        if len(PageNumber)>0:
            pNumber=str(int(PageNumber) + 16)
        else:
            pNumber='16'
        if 'limitstart' in url:
            url =url.split("&limitstart")[0]
        url+="&limitstart="+pNumber
        #addDir('Next Page' , url ,4,'',pageNum=pNumber)

        listToReturn.append({'name':'Next Page','url':url,'mode':mode,'iconimage':''})
    return listToReturn
	
def PlayShowLink ( url, name ): 
    list=getShowUrl(url); #cachinghere
    #print 'list',list
    if len(list)>0:
        urlToPlay=list["url"]
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
            #print 'youtubecode',youtubecode
            youtubecode=youtubecode[0]
            uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
            #print 'going to play',uurl;
        #    print uurl
            xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
    else:
        line1='Unable to find url'
        time=2000
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    return
    
def getShowUrl(url):
    line1="Fetching URL";
    time=2000
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

    link=getURL(url).result;
    match= re.findall('<param name="flashvars" .*?vid=(.*?)&amp*.?pid=(.*?)"', link)
    vidId=match[0][0]
    pid=match[0][1]
    url="http://www.pitelevision.com/index.php?option=com_allvideoshare&view=config&vid=%s&pid=%s&lang=en"%(vidId,pid)
    #print 'url',url
    link=getURL(url).result;
    #	print url
    match= re.findall('<video>(.*?)<', link)
    #print 'lowmatch', match
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
    urlToPlay=urlToPlay.replace(" ","%20")
    
    return {'url':urlToPlay}
    
	
		
    return

def getLiveUrl(url):
    line1="Fetching Live URL";
    time=2000
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

    #print 'fetching url',url
    link=getURL(url).result;
    match= re.findall('flashvars="src=(.*?)\.f', link)
    #print 'match',match
    url=""
    if len(match)>0:
        url=match[0]+'.m3u8'
    #print 'url',url
    return {'url':url}
    
    
        
    return	
#flashvars="src=(.*?)\.f

def PlayLiveLink ( url,name ): 
    urlDic=getLiveUrl(url)
  
    if not urlDic==None:
        line1="Url found, Preparing to play";
        time=2000
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

        playfile=urlDic["url"]
        #progress.update( 100, "", "Almost done..", "" )
        #print 'playfile',playfile
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        print "playing stream name: " + str(name) 
        xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( playfile, listitem)
    else:
          line1="Url not found";
          time=2000
          xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

    return


	
VIEW_MODES = {
    'thumbnail': {
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
    },
}

def get_view_mode_id( view_mode):
    view_mode_ids = VIEW_MODES.get(view_mode.lower())
    if view_mode_ids:
        return view_mode_ids.get(xbmc.getSkinDir())
    return None

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
    mode=urllib.unquote_plus(params["mode"])
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
    PageNumber=args.get('limitstart', '')[0]
except:
    PageNumber=''

if PageNumber==None: PageNumber=""


print     mode,url

		
try:

    if mode==None or url==None or len(url)<1:
        print "InAddTypes"
        Addtypes()

    elif mode=='VOD' or mode=='VODSerial':
        print "AddVOD url is ",name,url
        AddVOD(url,mode) #adds series as well as main VOD section, both are cat.

    elif mode=='VODEntry' or mode=='ALLC':
        print " AddEnteries Play url is "+url
        AddEnteries(url,PageNumber, mode)

    elif mode=='PlayVOD':
        print " PlayShowLink Play url is "+url
        
        PlayShowLink(url,name)
    elif mode=='PlayLive':
        print "Play url is "+url,mode
        PlayLiveLink(url,name)
    elif mode=='Settings':
        print "Play url is "+url,mode
        ShowSettings(url)
except:
    print 'something wrong', sys.exc_info()[0]
    traceback.print_exc()

if (not mode==None) and mode>1:
    view_mode_id = get_view_mode_id('thumbnail')
    if view_mode_id is not None:
        print 'view_mode_id',view_mode_id
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        print 'Container.SetViewMode(%d)' % view_mode_id
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))


