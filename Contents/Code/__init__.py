ParseStories = SharedCodeService.ParseStories.ParseStories

NPR_ROOT = 'http://api.npr.org'
API_KEY = 'MDAyNTU3MTA2MDEyMjk2NTE1MzEwN2U0MQ001'
LIST_URL = NPR_ROOT + '/list?apiKey=' + API_KEY
QUERY_URL = NPR_ROOT + '/query?id=%s&numResults=20&requiredAssets=audio&apiKey=' + API_KEY
SEARCH_URL = NPR_ROOT + '/query?startNum=0&sort=dateDesc&output=NPRML&numResults=20&apiKey=' + API_KEY

dirs = [
	# ['NPR Live Stream' , 'live'],
	['Topics', '3002'], 
	['Music Genres', '3018'], 
	['Programs' , '3004'],
	['Bios' , '3007'],
	['Music Artists' , 'music'],
	['Columns' , '3003'],
	['Series' , '3006']
]

musicDirs = [ ['Recent Artists', '3008'], ['All Artists', '3009'] ]

####################################################################################################

def Start():
	Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")

####################################################################################################
@handler('/music/npr', 'NPR')
def MainMenu():
	oc = ObjectContainer()
	for name, value in dirs:
		if value == 'music':
			oc.add(DirectoryObject(key=Callback(MusicMenu), title=name))
		# elif value =='live':
		# 	oc.add(DirectoryObject(key=Callback(PlayLive), title=name))
		else:
			oc.add(DirectoryObject(key=Callback(SectionMenu, id=value, name=name), title=name))
	oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.npr", title="Search", summary="Search NPR for...", prompt="Search for...",
		thumb=R("search.png")))
	return oc

####################################################################################################
@route('/music/npr/music')
def MusicMenu():
	oc = ObjectContainer(title2="Music Artists")
	for name, value in musicDirs:
		oc.add(DirectoryObject(key=Callback(SectionMenu, id=value, name=name), title=name))
	return oc

####################################################################################################
@route('/music/npr/section')
def SectionMenu(id, name):
	oc = ObjectContainer(title2=name)
	maxNumToReturn = 200
	for item in XML.ElementFromURL(LIST_URL + '&id=' + id).xpath('//item'):
		item_id = item.get('id')
		item_url = QUERY_URL % item_id
		item_title = item.xpath('./title')[0].text
		try:
			item_summary = String.StripTags(item.xpath('./additionalInfo')[0].text)
		except:
			item_summary = ''
		oc.add(DirectoryObject(key=Callback(ParseStories, url=item_url, name=item_title),
			title=item_title, summary=item_summary))
		if id == '3008':
			maxNumToReturn = maxNumToReturn - 1
			if maxNumToReturn <= 0: 
				break
	return oc

####################################################################################################
@route('/music/npr/live')
def PlayLive():
	oc = ObjectContainer()
	oc.add(TrackObject(url='http://npr.ic.llnwd.net/stream/npr_live24', title='NPR Live Stream', artist='NPR', album='24-Hour Program Stream', summary='NPR News and Shows'))
	return oc
