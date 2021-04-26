# -*- coding: utf-8 -*-
import wget
import os
from requests import get,post

#Svt news
url = "https://www.svt.se/nyheter/rss.xml"

rss_file = wget.download(url)

f = open(rss_file, 'r')
rssText = "\n".join(f.readlines())
f.close()

fullfeed = ""
count = 0

while True:
        try:
                rssTitle = rssText.split("<title>",1)[1]
                rssTitle = rssTitle.split("</title>",1)[0]
                rssText = rssText.split("<description>",1)[1]
                getfeed = rssText.split("</description>",1)[0]
                if (count > 0):
                        fullfeed += rssTitle.strip("\n") + ". " + getfeed.strip("\n")
                count += 1
                if count > 4:
                        break
        except:
                break


url = "http://HOMEASSISTANTIP:8123/api/services/tts/cloud_say"
myheaders = {
    "Authorization": "Bearer LONGLIVEDTOKEN",
    "content-type": "application/json",
}

mydata = '{"entity_id": "media_player.kok", "message": "' + fullfeed + '" }'

response = post(url, headers=myheaders, data=mydata)

#Remove creaded file
cmd = "rm rss_file"
os.system(cmd)
