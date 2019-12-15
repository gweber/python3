#!/usr/bin/python3
"""
This script reads temperatures from the Philips Hue Motion sensors and uploads them to a 
Google Drive sheet.  

You need
* a user in Google Developer Console for a project, with Google Drive API access as project editor
* the credentials stored locally as a json file
* a shared sheet in Google Drive
* the IP of your bridge ... https://www.meethue.com/api/nupnp or any other way
* a userhash from the bridge for accessing the API of the Hue bridge
* the ID of the temp sensors http://<ip_of_bridge>/api/<hashed_username_from_hue_bridge_for_ap/sensors/

Temperature is sent to the bridge every 5 minutes, so a cron job is best option.
Temperature is an int, convert to float /100
"""
import json, requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# hue sensors by static assignment 
sensors = {
       10: 'lving room',
       14: 'kitchen',
}

state_url = 'http://<ip_of_bridge>/api/<hashed_username_from_hue_bridge_for_ap/sensors/'

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('hue-user.json', scope)
client = gspread.authorize(creds)

# the sheet to add data to
sheet = client.open("hue temperature").sheet1
                    
for sensor_index, sensor_name in sensors.items():
    url = state_url + str(sensor_index)
    response = requests.get(url)
    device = response.json()
    #last update from sensor is stored in the bridge; temperature is an int, convert to float /100
    row = [str(device['state']['lastupdated']), sensor_index, sensor_name, device['state']['temperature']/100]
    sheet.append_row(row)
