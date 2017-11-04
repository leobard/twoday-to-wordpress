# Converting a twoday.net blog to wordpress xml

Written by Leo Sauermann

usage

1.export your blog from your twoday.net account into a textfile (administrate>weblog>import/export)
1.edit a lot of config on top of convert.py...
1.run script
    
	python3 convert.py twoday_2017-09-07-export-full-txt.txt > output.xml
	
## What for?
I wrote blog posts on http://leobard.twoday.net from 2004-03-26 to 2016-10-26, when I stopped blogging there. I want to keep the posts there for the record, but also move them to a self-hosted blog. I will continue blogging on a self-hosted wordpress on my private page leobard.net. It feels better for me to be able to have a copy of my blogposts I have written for years in a wordpress I host myself. I want to keep my blog my whole life and I want to keep publishing stuff in it, for example linked data. This is not possible on twoday. So I wrote a script to convert the export from twoday to wordpress. 

Twoday is an austrian blogging platform running since 2003 and still active. It is powered by helma/antville.http://twoday.net/ 

Twoday is provided by knallgrau (now called http://www.virtual-identity.com/, but I ignore this change for now as they also didn't bother changing their name on twoday). knallgrau, and knallgrau people and ex-knallgrau people did some amazing stuff besides twoday and I say: thanks to knallgrau for helping me to start blogging! Thanks for hosting my blog. 


## Images

* `<img>` tags are found
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
Fork it! Its MIT License. 

I, Leo Sauermann, am busy with other things and I don't need this script anymore as I used it to move my blog already. If you need support, you are out of luck. 

Pull requests: I have not much time to look at pull requests. It may take me years to accept them. Really, don't expect me to look at your pull request, I have tons of more interestng projects running and work to do. You could raise my attention with a bountysource greater than 20€ to look through it. Sounds stupid, but reflects my current plan to not support this project. Same with co-admins, I don't have time to judge your coding skills or ability to be a co-admin here. So if you want to be co-admin, raise my attention with a bountysource donation greater than 3€ and I am very happy to talk with you, hand this over, and make you the boss. You can also just fork it. 
