import pandas as pd
from pandas.io.json import json_normalize
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

print('Importing data...')

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
        
print('Data imported succesfully!')

activities = pd.json_normalize(all_activities)