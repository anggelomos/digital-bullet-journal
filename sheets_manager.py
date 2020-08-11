import pickle
import os.path
from datetime import date
from openpyxl.utils.cell import get_column_letter
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

    @property
    def spreadsheet_data(self):
        """ Return all the data available in the api method get.
        """
        return SheetsManager.sheet.get(spreadsheetId=self.gsheet_id, includeGridData=False).execute()

    @property
    def title(self):
        """ Return spreadsheet's title. 
        """
        return self.spreadsheet_data["properties"]["title"]

    def __repr__(self):
        return f"SheetsManager(gsheet_id='YourSpreadsheetID')"
    
    def __str__(self):
        return f"Title: {self.title}\nData: {self.values}"

    def read(self, cell_range: str) -> list:
        """Read cell values within the range specified in cells

        Parameters
        ----------
        cell_range : str
            Reading range. Ex. "A1:B2"

        Returns
        -------
        clean_read_values : list
            cell values converted into float if necessary. Ex. [["Hola", "Value"], [1.0, 2.0]]
        """
        result = SheetsManager.sheet.values().get(spreadsheetId=self.gsheet_id,
                                                  range=cell_range).execute()
        read_values = result.get('values', [])
        clean_read_values = []
        for row in read_values:
            clean_row = []
            for value in row:
                if len(value) > 0:
                    if value[0].isdigit():
                        clean_row.append(float(value))
                    else:
                        clean_row.append(value)
                else:
                    clean_row.append(value)
            clean_read_values.append(clean_row)
        return clean_read_values 

    def write(self, cell: str, data: list) -> dict:
        """Update cells starting in the cell according to the data

        Parameters
        ----------
        cell : str
            Starting cell. Ex. "A1"
        data : list(list)
            Data intended to write. Ex. [[1], [1, 1], [1]]

        Returns
        -------
        writing_result: dict
            Dictionary containing information about the writing operation. Ex. {'spreadsheetId': '1Hae-zhZKMY5PVWIipNWW7YgjS3ayWBi1jT93i46I5AE', 'updatedRange': 'Sheet1!F2:G4', 'updatedRows': 3, 'updatedColumns': 2, 'updatedCells': 4}
        """
        writing_data = {'values': data}
        writing_result = SheetsManager.sheet.values().update(spreadsheetId=self.gsheet_id,
                                                    range=cell,
                                                    body=writing_data,
                                                    valueInputOption='USER_ENTERED').execute()
        return writing_result

    @property
    def values(self):
        """ Return a list with all the values in the first sheet of the spreadsheet.
        """
        sheet_title = self.spreadsheet_data["sheets"][0]["properties"]["title"]
        sheet_values = self.read(cell_range=sheet_title)
        return sheet_values 


class DatabaseSheet(SheetsManager):
    def __init__(self, gsheet_id):
        super().__init__(gsheet_id)
    
    @property
    def headers(self):
        sheet_headers={}
        for index,row in enumerate(self.values):
            header = row[0]
            sheet_headers[header] = index+1
        return sheet_headers
        