# -*- coding: utf-8 -*-
import urllib
import os
import sys
from requests import get,post
import re
import subprocess

#How many news, default 1 in case of lost value
#numnews = int(sys.argv[1]), got it from the python call previously, now Home Assistant passes the number via MQTT call
numnews = 1

while True:
        #Make sure we wait for MQTT signal, by waiting for Mosquitto call
        #We are listening to "readnews"
        cmd = "mosquitto_sub -h HOMEASSISTANTIP -p 1883 -u homeassistant -P MQTTPASSWORD -t readnews -C 1"
        mqttreturn = subprocess.check_output(cmd, shell=True)
        
        #Make the return our new number of news to read
        numnews = int(mqttreturn)

        #Svt news
        url = "https://www.svt.se/nyheter/rss.xml"

        webf = urllib.urlopen(url)
        rssText = webf.read()

        ttsurl = "http://HOMEASSISTANTIP/api/services/tts/cloud_say"
        myheaders = {
            "Authorization": "Bearer HOMEASSISTANTLONGLIVEDTOKEN",
            "content-type": "application/json",
        }

        fullfeed = ""
        count = 0

        while True:
                try:
                        rssTitle = rssText.split("<title>",1)[1]
                        rssTitle = rssTitle.split("</title>",1)[0]
                        rssText = rssText.split("<description>",1)[1]
                        getfeed = rssText.split("</description>",1)[0]
                        if (count > 0):
                                fullfeed += rssTitle.strip("\n") + ". " + getfeed.strip("\n") + ". "
                                #mydata = '{"entity_id": "media_player.kok", "message": "' + rssTitle.strip("\n") + ". " + getfeed.strip("\n") + '" }'
                                #response = post(url, headers=myheaders, data=mydata)
                                #print(response.text)
                        count += 1
                        if count > numnews:
                                break
                except:
                        break

        #Remove all strange characters
        fullfeed = re.sub(r'[^ åäöÅÄÖa-zA-Z0-9\._-]', '', fullfeed)

        mydata = '{"entity_id": "media_player.kok", "message": "' + fullfeed + '" }'


        response = post(ttsurl, headers=myheaders, data=mydata)
        #print(mydata)
        print(response.text)
