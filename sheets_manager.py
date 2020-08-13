import pickle
import os.path
import datetime
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
                try:
                    if value[0].isdigit():
                        clean_row.append(float(value))
                    else:
                        clean_row.append(value)
                except :
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
    def __init__(self, gsheet_id, static_headers: list=["month", "week", "day", "date"]):
        super().__init__(gsheet_id)
        self.static_headers = static_headers
    
    @property
    def headers(self):
        """ Return the first value of each row.
        """
        sheet_headers=[]
        for index,row in enumerate(self.values):
            if row == []:
                header = ''
            else:
                header = row[0]
            sheet_headers.append([header, index+1])
        return sheet_headers

    @property
    def labels(self):
        labels = self.headers.copy()
        for header in self.headers.keys():
            if header in self.static_headers:
                labels.pop(header, None)
        return labels

    def date_column(self, requested_date:str) -> str:
        """Return the column A1 notation in the database for the requested date.

        Parameters
        ----------
        requested_date : str
            Date in ISO 8601 format YYYY-MM-DD. Ex. 2020-12-05

        Returns
        -------
        Column_A1_notation: str
            A1 Notated column corresponding to the requested date in the database. Ex. XB
        """
        split_date = requested_date.split("-")
        split_date = [int(value) for value in split_date]
        delta_days = datetime.date(split_date[0], split_date[1], split_date[2]) - datetime.date(2020, 8, 10)
        days_between = delta_days.days
        return get_column_letter(days_between+2)

    def week_data(self, requested_date: str) -> list:
        """ Return a list with the week number and the monday date in ISO 8601 of the week containing the requested_date.

        Parameters
        ----------
        requested_date : str
            Date in ISO 8601 format contained in the week.

        Returns
        -------
        week_data : list
            list with the week number and the monday date in ISO 8601 of the week containing the requested_date. Ex. [33, '2020-08-10'
        """
        split_date = requested_date.split("-")
        split_date = [int(value) for value in split_date]
        requested_date = datetime.date(split_date[0], split_date[1], split_date[2])

        _,week_number,_ = requested_date.isocalendar()
        monday_date = requested_date - datetime.timedelta(days=requested_date.weekday())

        return [week_number, str(monday_date)]
    