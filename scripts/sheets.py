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
    def __init__(self):
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]
        self.file_name = Settings().getFileName()
        self.credential_path = "/".join([os.path.dirname(os.path.abspath("client_secret.json")),
                                         "client_secret.json"])
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credential_path, self.scope)
        self.gc = gspread.authorize(self.credentials)

    def setFileName(self, ws_name):
        try:
            self.gc.open(ws_name)
            self.file_name = ws_name

            return "Changed spreadsheet file name to {}".format(ws_name)
        except:
            return "Cannot find file with {}".format(ws_name)

    def addGSheetsRow(self, data):
        # adds total price = quantity * price per unit
        data.append(data[2] * data[3])

        # insert the date as first element
        date = datetime.datetime.now()
        data.insert(0, "/".join([str(date.month), str(date.day), str(date.year)]))

        # get the 'Purchasing List' worksheet
        purchasing_list_ws = self.gc.open(self.file_name).get_worksheet(1)

        #purchasing_list_ws.resize(1)
        purchasing_list_ws.append_row(data)

        assert isinstance(data, list)
