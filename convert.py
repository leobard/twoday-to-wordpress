# convert antville helma to wordpress import/export XML
# author leo sauermann
# date 4.11.2017
# license: https://opensource.org/licenses/MIT because its so short and easy
# doc see README.md

# Doc good to have when coding
# https://codex.wordpress.org/Importing_Content

import sys
from datetime import *
from collections import Counter
from collections import defaultdict 
import cachehtmlimages


###
### -------------------- A LOT OF CONFIGURATION --------------------
###

# Wrap Body in CDATA section. True/false
cfg_wrapbodywithcdata = True
# Cache for downloaded images
cfg_localprefix='/2017/imgcache/'
cfg_cachedir='cachedir'
cfg_enablecache=True
cfg_channelboilerplate='''<channel>
<title>Export file</title>
<link>http://www.example.com/blog</link>
<description>Just another WordPress site</description>
<pubDate>Fri, 20 Oct 2017 21:08:14 +0000</pubDate>
<language>en-US</language>
<wp:wxr_version>1.2</wp:wxr_version>
<wp:base_site_url>http://www.example.com/blog</wp:base_site_url>
<wp:base_blog_url>http://www.example.com/blog</wp:base_blog_url>
<wp:author><wp:author_id>1</wp:author_id><wp:author_login><![CDATA[leobard]]></wp:author_login><wp:author_email><![CDATA[the@leobard.net]]></wp:author_email><wp:author_display_name><![CDATA[leobard]]></wp:author_display_name><wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>
'''
cfg_wpposttype='post'
# add the TITLE(s) of blogpost(s) here if you want to get an XML file with just these posts
cfg_importonly=[]


spammers = []
spammerwithcomments = defaultdict(list)

whitelist = {'leobard': 68, 'Chris Mark': 5, 'lucasswonn': 5, 'Donmoss': 4, 'humtum': 3, 'peter andersson': 3, 'antheque': 2, 'Tony Lara': 2, 'Guenther (guest)': 2, 'Martincrow': 2, 'darrensy': 2, 'Lars Zapf (guest)': 2, 'danja': 2, 'sherman': 2, 'Fernandro': 2, 'kollektivtraeumer': 1, 'Max V&ouml;lkel (guest)': 1, 'jip': 1, 'Anja Jentzsch (guest)': 1, 'BrettspielBrowser': 1, 'Jeen (guest)': 1, 'heimwege (guest)': 1, 'Richard Cyganiak (guest)': 1, 'kabsi (guest)': 1, 'Gunnar (guest)': 1, 'tim finin (guest)': 1, 'D.E.R. Kabsi (guest)': 1, 'Arne (guest)': 1, 'Gunnar Grimnes (guest)': 1, 'typekey:Dan Brickley': 1, 'xamde': 1, 'guenthernoack': 1, 'Dan Connolly (guest)': 1, 'Heimwege (guest)': 1,
'020200 (guest)':1, "anonymous (guest)":1, 'Sramana Mitra (guest)':1,
"karl (guest)":1,
"020200":1,
"Laurens Holst (guest)":1,
"Webmaster (guest)":1,
"Bernhard (guest)":1,
"komm.rip":1,
"Damian (guest)":1,
"Jan (guest)":1,
"smi":1,
"Laurent Szyster (guest)":1,
"Frank (guest)":1,
"pavel (guest)":1,
"simsplayah":1,
"reubenk":1,
"Andreas (guest)":1,
"Dave Brondsema (guest)":1,
"jariep":1,
"laurentszyster":1,
"Dominik (guest)":1,
"Maggi (guest)":1,
"SiENcE (guest)":1,
"Ed Davies (guest)":1,
"Pavel9":1,
"Martin (guest)":1,
"D.E.R.":1,
"feedbuzz":1,
}


blacklist = {
"musicindance",
"richardphillips8416",
"myspainholidays",
"Alstair",
"samsameer",
"aliyog",
"enthusiast225",
"rosepdtr",
"hyunnonu",
"boulevardsg",
"flywithme",
"bankhing",
"Martink23",
"rodhildred",
"julioman",
"Ben67",
"adam434",
"arnoldcarrington",
"Bojobycy",
"jonz",
"John_smith",
"ashish9454",
"milos01011984",
"nanziecane",
"jmorris14",
"denzie",
"Caouette",
"recadolee",
"dmolvik",
"smithbell",
"rockyhenry",
"tsonga1198",
"AwningsForHomes",
"buntagna",
"kumar",
"larrzz0jh",
"stenlyanson",
"thomasfernandus",
"jansenkoe (guest)",
"tradetuber",
"plantar exercises",
"jeanalbert2018",
"mercymac19",
"benostill",
"pele092131",
"pdambc163",
"granicefer11",
"laneejakona",
"catarina09183",
"nike2636",
"thestars",
"longma",
"artedavida",
"jolina",
"johntlr",
"stevensegal60",
"Latos354",
"amhash",
"razibjohn",
"anna9871",
"geogia987",
"JackWitson",
"heartofqueen",
"voansumer",
"tqbcl36",
"zakoment",
"mliege",
"erwinhector",
"miltonm103",
"flashwd",
"Caouette1",
"NatalieWilliam99",
"fyodorsteven",
"johnluv",
"lisaok",
"mario98121",
"jonathan200",
"mahmoud321",
"Anna Marie",
"davidchair34",
"macmercy",
"juz2maryu",
"hamza123",
"lhc67",
"alat kesehatan",
"pollockshaun",
"fgermanyer",
"speednews.it (guest)",
"davidguez",
"netbrainiac",
"Kerson",
"isha",
"jackdiamond",
"jameskeaton",
"adelaidetaylor",
"alinsmith",
"JamesRobert",
"yuzz3n",
"yoyo7",
"JonathanAquino",
"reigna",
"christina12",
"bista675",
"raffyprince",
"alex46 (guest)",
"ssasoo",
"sinthia_jaman",
"evawagner87 ",
"authority216",
"jamezlee",
"nursebebo",
"Swampthing (guest)",
"starplayer",
"usabta",
"Supreme",
"Bratish175",
"helentarlow",
"sdfdsf (guest)", 
"golfwholesaler18",
"Marry444",
"beckham1291",
"johnrock",
"zinlosho",
"patrickbest",
"DavidJohn",
"george22","thomasdelange","george22","alton100","Roberdro", "miketyson986", "miketyson986","jerry.nic","alec7334","jauhis", "jessiejames","esmi25","mortage","alton100", "miketyson986",'susanbell84','danleyvila','Rainer (guest)','nabihahayat','wify','sarahjames786','Samii', "jesika",
"johndecoza",
"Yuichi Junigida",
"vanessa198012","alex0012",
"attain98",
"bellegardner",
"celinedion201982","asim",
"123akshay",
"geraldrss",
"sads",
"swatbolish",
"Alex11",
"katebroad21",
"StevenJ",
"jessica098",
"Leetony2598",
"Emma Lue",
"lam",
"PSteve",
"rsweeting123",
"mortage35",
"coach001",
"Allysonrock3",
"fdgdf (guest)",
"smackshown",
"NathalieD",
"rihanna09413",
"lindasmithsons",
"Jared H.",
"Duagiibii",
"keantommy",
"Amandavarley",
"seenathkumar",
"joshkurtis",
"mandybeck",
"Larah",
"lacomunicacion",
"SonicB",
"JorkRodan",
"yesyes",
"jhonmgt745",
"reactor67",
"ethak",
"fenny",
"tintly",
"alijutt8",
"mendadesantos",
"ladykippy",
"mammer",
"waxx7",
}

# replace these image filenames in the body because they lacked the extension #hack
# TODO: this hack could be replaced by making the cachehtmlimages.py evaluate the file-ending, the content-type, and doing the right thing when downloading. Would take more than 60 minutes though to code and this was 5 mintues.
cfg_rplc={
'http---leobard.twoday.net-getfile-name-IMG_8468':'http---leobard.twoday.net-getfile-name-IMG_8468.jpg',
'http---leobard.twoday.net-getfile-name-IMG_8468':'http---leobard.twoday.net-getfile-name-IMG_8468.jpg',
'http---wordle.net-thumb-wrdl-216762-leobards_delicious':'http---wordle.net-thumb-wrdl-216762-leobards_delicious.jpg',
'http---www.w3.org-Icons-w3c_home':'http---www.w3.org-Icons-w3c_home.png',
'http---www.flickr.com-images-buddyicon.jpg-91744463-N00':'http---www.flickr.com-images-buddyicon.jpg-91744463-N00.jpg',
'http---static.flickr.com-23-buddyicons-96533977-N00.jpg-1123189502':'http---static.flickr.com-23-buddyicons-96533977-N00.jpg-1123189502.jpg',
'http---bugs.kde.org-attachment.cgi-id-11622-action-view':'http---bugs.kde.org-attachment.cgi-id-11622-action-view.jpg',
'http---ep.yimg.com-ca-I-yhst-81571646212247_2099_760690':'http---ep.yimg.com-ca-I-yhst-81571646212247_2099_760690.gif',
'http---ep.yimg.com-ca-I-yhst-81571646212247_2101_64972':'http---ep.yimg.com-ca-I-yhst-81571646212247_2101_64972.gif',
}


###
### -------------------- CONFIGURATION ENDS, THE REST IS CODE --------------------
###

# remove funny characters in a body and fix image filenames where we dont have an extension #hack
def sanitizebody(body):
	for i,ii in cfg_rplc.items():
		body=body.replace(i,ii)
	body=body.replace('', ' ')
	return body

def nicename(s):
	return s.lower().replace(' ','-')

filename = sys.argv[1]
with  open(filename) as fp:
	contents = fp.read()
	print ('<?xml version="1.0" encoding="UTF-8" ?>')
	print ('<!-- generator="Helma-Antville to wordpress Converter" created="'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'" -->')
	print ('''<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>''')
	print (cfg_channelboilerplate)
	print ('<generator>https://www.leobard.net/2017/helma-to-wordpress</generator>')

	for entry in contents.split('\n-----\n--------\n'):
		# do something with entry  
		if len(entry)==0:
			continue
		headerAndBody = entry.split('\n-----\nBODY:\n')
		header = headerAndBody[0]
		try:
			body = headerAndBody[1]
		except Exception as e:
			print (e)
			print (headerAndBody)
			raise (e)
		
		# parse headers
		headeritems={}
		for headerline in header.split('\n'):
			try:	
				key,value = headerline.split(': ',1)
				try:
					if (key=='DATE'):
						value = datetime.strptime(value, '%m/%d/%Y %I:%M:%S %p')
				finally:
					headeritems[key]=value
			except Exception as e:
				print (e)
				print (headerline)
				raise (e)
		
		if (len(cfg_importonly) > 0) and (not(headeritems['TITLE'] in cfg_importonly)):
			continue
		
		# print item
		print ('	<item>')
		print ('		<title><![CDATA['+headeritems['TITLE']+']]></title>')
		#                                                       Tue, 08 Feb 2011 00:00:00 +0000
		print ('		<pubDate>'+headeritems['DATE'].strftime('%a, %d %b %Y %H:%M:%S +0000')+'</pubDate>')
		print ('		<dc:creator><![CDATA['+headeritems['AUTHOR']+']]></dc:creator>')
		isodate = headeritems['DATE'].strftime('%Y-%m-%d %H:%M:%S')
		print ('		<wp:post_date><![CDATA['+isodate+']]></wp:post_date>')
		print ('		<wp:post_date_gmt><![CDATA['+isodate+']]></wp:post_date_gmt>')
		print ('		<wp:post_type><![CDATA['+cfg_wpposttype+']]></wp:post_type>')
		# nicename
		print ('		<category domain="category" nicename="'+nicename(headeritems['CATEGORY'])+'"><![CDATA['+headeritems['CATEGORY']+']]></category>')
		
		bodyAndComments = body.split('\n-----\nCOMMENT:\n')
		if not (bodyAndComments) or	(len(bodyAndComments)==1):
			body = bodyAndComments[0]
			comments = []
		else:
			body = bodyAndComments[0]
			comments = bodyAndComments[1:]
			
		
		# BODY: cache images?
		if cfg_enablecache:
			try:
				body = cachehtmlimages.localifyHtmlImages(body, cfg_localprefix, cfg_cachedir)
			except Exception as e:
				sys.stderr.write(str(e)+'\n')
				sys.stderr.write('This was during cachehtmlimages of item with date '+isodate+'. Continuing...\n')
		
		# BODY: sanitize XML
		body = sanitizebody(body)
		
		print ('		<content:encoded>')
		if (cfg_wrapbodywithcdata):
			print ('<![CDATA[')
		print (body)
		if (cfg_wrapbodywithcdata):
			print (']]>')
		print ('		</content:encoded>')
			
		# THERE ARE COMMENTS. TURN THEM INTO HTML
		if len(comments)>0:
			tt = ''
			for comment in comments:
				commentheaders = {}
				commentlines = comment.split('\n')
				if (commentlines[0]=='REPLY:'):
					reply=1
					i=1
				else:
					reply=0
					i=0
				while i<len(commentlines):
					try:
						key,value = commentlines[i].split(': ',1)
					except Exception as e:
						sys.stderr.write(str(e))
						sys.stderr.write('\n'+commentlines[i]+'\n')
						raise e
					if key=='AUTHOR':
						author=value
					if key=='DATE':
						# unlike with the item, I transform the comment date directly to ISO as I don't need it in any other format
						try:
							m2 = datetime.strptime(value, '%m/%d/%Y %I:%M:%S %p')
							value = m2.strftime('%Y-%m-%d %H:%M:%S')
						except Exception as e:
							sys.stderr.write(str(e))
							sys.stderr.write('\n'+commentlines[i]+'\n')
						# DATE also marks the end of the header of the comment, the rest is content-body
						commentbody = '\n'.join(commentlines[(i+1):])
						i = len(commentlines) # exit this loop
					commentheaders[key]=value
					i += 1
				if author in blacklist:
					continue
				# Spam detection: Read the comment and find hrefs to collect a list of possible spammers
				spamham = commentbody.lower()
				if ('href' in spamham):
					if not author in whitelist:
						# make commentbody easier to read to judge if spam
						spamham = spamham.replace('\n', ' ')
						spamham = spamham[spamham.index('href'):]
						spammers.append(author)
						spammerwithcomments[author].append(spamham)
						continue
				
				# print the comment
				print ('		<wp:comment>')
				print ('			<wp:comment_author><![CDATA['+commentheaders['AUTHOR']+']]></wp:comment_author>')
				print ('			<wp:comment_author_url><![CDATA['+commentheaders['EMAIL']+']]></wp:comment_author_url>')
				print ('			<wp:comment_date><![CDATA['+commentheaders['DATE']+']]></wp:comment_date>')
				print ('			<wp:comment_date_gmt><![CDATA['+commentheaders['DATE']+']]></wp:comment_date_gmt>')
				print ('			<wp:comment_content><![CDATA['+sanitizebody(commentbody)+']]></wp:comment_content>')
				print ('			<wp:comment_approved><![CDATA[1]]></wp:comment_approved>')
				print ('		</wp:comment>')			
		
		print ('	</item>')
		# break
	print ('</channel>')
	print ('</rss>')

# Print out the stuff about people who posted <a href> but are not in whitelist or blacklist
for k,l in spammerwithcomments.items():
	sys.stderr.write('"'+k+'", \n')
	for i in l:
		sys.stderr.write('	'+i[:110]+'\n')
if len(spammers) > 0:
	sys.stderr.write(str(Counter(spammers)))
