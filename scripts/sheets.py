import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connectGSheets():

    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]

    # get path to client_secret.json
    path = "/".join([os.path.dirname(os.path.abspath("client_secret.json")),"client_secret.json"])

    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)

    gc = gspread.authorize(credentials)

    return gc


def addGSheetsRow(data):

    gc = connectGSheets()

    # adds total price = quantity * price per unit
    data.append(data[2] * data[3])

    # insert the date as first element
    date = datetime.datetime.now()
    data.insert(0, "/".join([str(date.month), str(date.day), str(date.year)]))

    # get the 'Purchasing List' worksheet
    purchasing_list_ws = gc.open("MDRC - Ledger 2019/20").get_worksheet(1)

    #purchasing_list_ws.resize(1)
    purchasing_list_ws.append_row(data)

    assert isinstance(data, list)
