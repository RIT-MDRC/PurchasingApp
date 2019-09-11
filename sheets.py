'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Functions to do google sheets operations
'''
import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GSheetsAgent:
    def __init__(self, settings):
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]
        self.file_name = settings.getFileName()
        self.credential_path = "/".join([os.path.dirname(os.path.abspath("client_secret.json")),
                                         "client_secret.json"])
        # self.credential_path = os.path.abspath("client_secret.json")
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credential_path, self.scope)
        self.gc = gspread.authorize(self.credentials)

    def addGSheetsRow(self, data):
        # adds total price = quantity * price per unit
        print(data)
        data.append(data[3] * data[4])

        # insert the date as first element
        date = datetime.datetime.now()
        data.insert(0, "/".join([str(date.month), str(date.day), str(date.year)]))

        try:
            # get the 'Purchasing List' worksheet
            purchasing_list_ws = self.gc.open(self.file_name).get_worksheet(self.getWorksheet("purchasing_list"))
            purchasing_list_ws.append_row(data)

            return True

        except:
            return False

    def getWorksheet(self, sheet_name):

        if sheet_name == "ledger":
            return 0
        elif sheet_name == "purchasing_list":
            return 1
        elif sheet_name == "purchasing_checklist":
            return 2
        else:
            return None