import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
gc = gspread.authorize(credentials)

df = pd.read_csv('/Users/jairusmartinez/Desktop/Python_Data_Analysis /Strava/strava_data.csv')

spreadsheet_key = '1cN18XshR_r-xvRGJiW0qU8dKP6amzsm8amPHXgLmRyg'
wks_name = 'StravaData'
d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
