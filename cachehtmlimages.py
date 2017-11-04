# download images mentioned in html and change the html to reflect a new image URI
# author leo sauermann
# date 4.11.2017
# license: https://opensource.org/licenses/MIT because its so short and easy

import sys
import re
import os
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import shutil
from pathlib import Path

'''
simplest usage example:

import cachehtmlimages
b = '<p>this<b>fat</b></p><p>cat<br/><br/>jumpsthefox</p><img src="https://upload.wikimedia.org/wikipedia/commons/8/8f/FoxJumpingDog.PNG"/>'
cachehtmlimages.localifyHtmlImages(b,'/publicurltocachefolder/','localcachedir')
'''

# Take a URL and turn it into a filename that can work on windows.
def urltofilename(url, length=255):
	# localify filename
	localifiedname = re.sub(r'[^a-zA-Z0-9\.\-_]', '-', url)
	# Max length filename 255 in Windows
	if len(localifiedname) > length:
		localifiedname = localifiedname[:(length-20)] + '...' + localifiedname[-17:]
		if len(localifiedname) != length:
			raise Exception('Leo, you did it wrong. Localifiedname: '+str(localifiedname))
	return localifiedname

# Download image from URL, save it to cachedir, prefix it with localprefix
# Mangle the image URL deterministically into a local filename for convenient lookup ("localify
# Return a URL that should be embedded as SRC for an IMG tag
# Example: cacheimg('https://upload.wikimedia.org/wikipedia/commons/8/8f/FoxJumpingDog.PNG', '/publicurltocachefolder/', 'localcachedir', 2)
def cacheimg(url, localprefix, cachedir):
	# ensure cachedir
	cachedir = Path(cachedir)
	if not cachedir.exists():
		os.makedirs(cachedir)
	
	# how would we name this url as a file?
	localifiedname = urltofilename(url, 251)
		
	# file already there? return it
	fp = Path(cachedir) / localifiedname
	if fp.exists():
		return localprefix + localifiedname
	
	# 404 before?
	fp404 = Path(cachedir) / (localifiedname + '.404')
	if fp404.exists():
		# 404? document unsuccessful download. return original URL, this is hopeless
		return url
		
	# download
	try:
		with urllib.request.urlopen(url) as response, fp.open('wb') as out_file:
			shutil.copyfileobj(response, out_file)
			return localprefix + localifiedname
	except urllib.error.HTTPError as e:
		# Return code error (e.g. 404, 501, ...)
		# ...
		print('Error downloading ' + url + ': ' + str(e.code) + '. Marking file as 404 by generating ' + str(fp404) +'. Returning original URL as recommended IMG src.')
		fp404.touch()
		return url
	except Exception as e:
		print('Error downloading ' + url + ': ' + str(e.code) + '. Raising the Exception.')
		raise e
	

def localifyHtmlImages(body, localprefix, cachedir):
	soup = BeautifulSoup(body, 'html.parser')
	for img in soup.find_all('img'):
		cachedurl=cacheimg(img['src'], localprefix, cachedir)
		img['src'] = cachedurl

	return str(soup)
