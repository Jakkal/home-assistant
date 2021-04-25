# -*- coding: utf-8 -*-
from requests import get,post

# Python-script to send Text to speach to Home assistant. Works well with longer texts. For example a newsfeed.
# This example just shows the basic mechanism of how TTS is sent to Home assistant.
#
# PRE-REQUIREMENTS!
# You need to edit your configuration.yaml file and add:
#
# api:
#
# This will make it possible to do API calls, like we want to do here
#
# In my example i use the "cloud_say" as TTS service. You can use Google_say or any other TTS integration
# in Home assistant. If you are unsure what to type. Make a small script with the Home assistant interface,
# and check the YAML code. If it says:
# tts:
#   cloud_say:
#      ....
# Then you add "/tts/cloud_say" after the api/services/ in the URL below
#
url = "http://HOMEASSISTANTIP:8123/api/services/tts/cloud_say"

#
# To obtain Homeassistant long lived token follow this tutorial:
# https://www.atomicha.com/home-assistant-how-to-generate-long-lived-access-token-part-1/
# Don't change the text "Bearer" - it's not a user, it should say "Bearer"
#
myheaders = {
    "Authorization": "Bearer HOMEASSISTANTLONGTOKEN",
    "content-type": "application/json",
}

mymessage = "Here is your long TTS message. You can scrap RSS or other text material to send long TTS messages to your home assistant"

# Entity_id refers to the mediaplayer on witch you want the TTS to be spoken to.
mydata = '{"entity_id": "media_player.kitchen", "message": "' + mymessage + '" }'

#Response is the Home assistant respons.
response = post(url, headers=myheaders, data=mydata)
print(response.text)
