import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SheetsManager:
    
    def __init__(self, gsheet_id):
        self.gsheet_id = gsheet_id

    gsheet_scope = ['https://www.googleapis.com/auth/spreadsheets']
    gsheet_creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gsheet_credentials//token.pickle'):
        with open('gsheet_credentials//token.pickle', 'rb') as token:
            gsheet_creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not gsheet_creds or not gsheet_creds.valid:
        if gsheet_creds and gsheet_creds.expired and gsheet_creds.refresh_token:
            gsheet_creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gsheet_credentials//sheet_credentials.json', gsheet_scope)
            gsheet_creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gsheet_credentials//token.pickle', 'wb') as token:
            pickle.dump(gsheet_creds, token)

    service = build('sheets', 'v4', credentials=gsheet_creds)
    sheet = service.spreadsheets()

    def write(self, cell: str, data: list) -> dict:
        writing_data = {'values': data}
        writing_result = SheetsManager.sheet.values().update(spreadsheetId=self.gsheet_id,
                                                    range=cell,
                                                    body=writing_data,
                                                    valueInputOption='USER_ENTERED').execute()
        return writing_result