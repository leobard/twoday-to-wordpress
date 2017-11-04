# Converting a helma/antville blog to wordpress xml

Written by Leo Sauermann

usage

    edit a lot of config on top of convert.py...
    
	python3 convert.py twoday_2017-09-07-export-full-txt.txt > output.xml
	

## Images

* <img> tags are found
* the src is read to find the image URL
* the img URL is downloaded to folder cfg_cachedir
* the img URL is transformed into a file-name
* it is assumed you upload all these files from the cachedir to your webserver to a folder that will exist forever. If you don't know what that is, read [Cool URIs don't change](https://www.w3.org/Provider/Style/URI) for examples.
* set the URL of the folder that exists forever into cfg_localprefix
* For images that were not retrieved with a file extension, add a file extension yourself. Then edit cfg_rplc to tell the script what filename replacements it needs to do.

## Spam

* Twoday.net is beaten by spammers, hard
* The script contains a whitelist where friends should be added and a blacklist where spammers are to be added
* The script will write all authors and their html to system.err if a link is in the html, unless they show up in whitelist or blacklist. Use the output to move names to either whitelist or blacklist. Once all friends are in whitelist and spammers in blacklist, output will stop

## Boilerplate
* edit cfg_channelboilerplate

## (No) Support

I, Leo Sauermann, am busy with other things and I don't need this script anymore as I used it to move my blog already. If you need support, you are out of luck. 

Pull requests: I am happy to accept pull requests if you send them over. It may take years to accept them, though. If you insist, first make a bountysource donation > 20€ and I will sit down and look through it. Sounds stupid, but reflects my current plan to support this project (no support planned). Same with co-admins, I don't have time to judge your coding skills or ability to be a co-admin here. So if you want to be co-admin, raise my attention with a bountysource donation > 3€ and I am happy to talk. 

I am aware this script may be interesting for some people who plan to copy their content from twoday.net or other helma/antville platforms to wordpress. If you are in this situation - this script may help if you can program python. But I can't help.
