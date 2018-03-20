'''
service help you to easy create, modify, delete, get googlesheet

Created on 2018年3月18日
@author: rocky.wang
'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


class GooglesheetService():
    
    service = None
    spreadsheetId = None

    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        # init service
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

        
    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: 
                # Needed only for compatibility with Python 2.6
    #             credentials = tools.run(flow, store)
                print("pass")
            print('Storing credentials to ' + credential_path)
        return credentials



    ''' add a new sheet and return sheetId '''
    def addSheet(self, title):
        body = {
          "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title,
                        }
                    }
                }
            ]
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body)
        response = request.execute()
        return response["replies"][0]["addSheet"]["properties"]["sheetId"]

    def deleteSheet(self, sheetId):
        body = {
            "requests": [
                {
                  "deleteSheet": {
                    "sheetId": sheetId
                  }
                }
            ]
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body)
        response = request.execute()
        print(response)
    
    
    def updateSheet(self, rangeName, rowList):
        body = {
            "values" : rowList
        }
        result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, range=rangeName, valueInputOption="RAW", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')));
        print("%s" %(json.dumps(result, indent=4)))
    
    def appendSheet(self, rangeName, rowList):
        body = {
            "values" : rowList
        }
        result = self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId, range=rangeName, valueInputOption="RAW", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')));
        
        print("%s" %(json.dumps(result, indent=4)))
    
    
    def clearSheet(self, rangeName):
        self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=rangeName, body={}).execute()
    
    # TODO get all sheet datas
    
    
    
    
    
    
    

