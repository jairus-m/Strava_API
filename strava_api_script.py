import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import datetime as dt
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "101957",
    'client_secret': 'ec468b20c28976c02db5577ff56bb47468fac246',
    'refresh_token': '11a38b5d320a34ce9e728968ed26441e5c024330',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}


page_list = list(np.arange(1,11))
all_activities = []

for request_page_number in page_list:
    param = {'per_page': 200, 'page':request_page_number}
    my_dataset = (
        requests.get(activites_url, headers=header, params=param).json()
        )
    
    if len(all_activities) == 0:
        all_activities = my_dataset
        print(f'Copying Page: {request_page_number}')
    else:
        all_activities.extend(my_dataset)
        print(f'Copying Page: {request_page_number}')
        
print('Finished.')

activities = pd.json_normalize(all_activities)

drop_columns = ['start_date','resource_state', 'type', 'start_date', 
                'timezone', 'utc_offset', 'location_city', 'location_state', 
                'location_country', 'photo_count', 'trainer', 'commute',
                'manual', 'flagged', 'gear_id', 'start_latlng', 'end_latlng', 
                'heartrate_opt_out', 'display_hide_heartrate_option', 
                'upload_id', 'upload_id_str', 'external_id', 
                'from_accepted_tag', 'total_photo_count', 'athlete.id',
                'athlete.resource_state', 'map.id', 'map.summary_polyline',
                'map.resource_state', 'device_watts', 'workout_type', 
                'average_temp']

df = activities.drop(columns=drop_columns)

def sec_to_min(x):
        minutes =  x / 60
        return round(minutes,2)

def meters_to_miles(x):
    miles = x / 1609.344 
    return round(miles, 2)

def meters_to_feet(x):
    feet = x * 3.28084
    return round(feet, 2)

def mps_to_mph(x):
    mph = x * 2.23694
    return round(mph, 2)    

df['distance'] = meters_to_miles(df['distance'])
df['moving_time'] = sec_to_min(df['moving_time'])
df['elapsed_time'] = sec_to_min(df['elapsed_time'])
df['total_elevation_gain'] = meters_to_feet(df['total_elevation_gain'])

df['date'] = df['start_date_local'].astype('datetime64')
df = df.drop(columns='start_date_local')
df['time'] = df['date'].dt.hour
df['time_bins'] = pd.cut(
    df['time'],
    bins=[0,4,8,12,16,20,24],
    labels=['12-4am', '4am-8am', '8am-12pm', '12pm-4pm', '4pm-8pm', '8pm-12am'],
    ordered=True
)

df['average_speed'] = mps_to_mph(df['average_speed'])
df['max_speed'] = mps_to_mph(df['max_speed'])
df['run_pace'] = 60 / df['average_speed']

df['elev_high'] = meters_to_feet(df['elev_high'])
df['elev_low'] = meters_to_feet(df['elev_low'])


df.to_csv('/Users/Jairusmartinez/Desktop/Python_Data_Analysis /Strava/strava_data.csv', index=False)             


