import pandas as pd
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

clientId = str(input("Please enter the Google API client ID:"))
clientSecret = str(input("Please enter the Google API secret"))
listLocation = str(input("Please enter the exact location of the list containing the websites to be added to your property"))

df = pd.read_excel(listLocation, sheet_name=0) # Specify the sheet
website_list = df['Complete URL'].tolist() # Get the list name
website_list_clean = [website for website in website_list if str(website) != "nan"]

OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters'

# Google retired the copy-paste (out-of-band) OAuth flow, so sign-in now goes
# through a temporary local redirect: a browser opens, you approve, done.
flow = InstalledAppFlow.from_client_config(
    {'installed': {
        'client_id': clientId,
        'client_secret': clientSecret,
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
    }},
    scopes=[OAUTH_SCOPE],
)
credentials = flow.run_local_server(port=0)

webmasters_service = build('webmasters', 'v3', credentials=credentials)

for website in website_list_clean:
  try:
    webmasters_service.sites().add(siteUrl=website).execute()
  except Exception as err:
    print(f'Other error occurred: {err}')
  else:
    print(website+" has been added to your GSC!")
    time.sleep(5)