import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def authenticate(SCOPES):
    creds = None  # no login yet

    token_data = os.getenv('GMAIL_TOKEN')  # check if running on Railway (cloud)

    if token_data:
        # Railway: load token from environment variable instead of file
        creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)

    elif os.path.exists('token.json'):
        # Local: load saved login from token.json file
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:  # no login OR login expired
        
        if creds and creds.expired and creds.refresh_token:
            # token expired → silently renew it without browser popup
            creds.refresh(Request())

        else:
            # no token at all → open browser for fresh Google login
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # opens browser popup

        # save new token to file (works locally, ignored on Railway)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())  # convert credentials object → JSON string → save

    return creds  # return valid login to gmail_classifier.py
