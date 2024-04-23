from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaInMemoryUpload
from google.oauth2 import service_account
import traceback
import os
import mimetypes

class SheetsLib:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self,version = "v4"):
        self.DRIVE = None
        self.version = version

    def connectDrive(self,authFile,storageFile="",isServiceAccount=False):
        try:
            if not isServiceAccount:
                store = file.Storage(storageFile)
                creds = store.get()
                if not creds or creds.invalid:   
                        flow = client.flow_from_clientsecrets(authFile, self.SCOPES)
                        creds = tools.run_flow(flow, store)
                self.DRIVE = discovery.build('sheets', self.version, http=creds.authorize(Http()))
            else:
                credentials = service_account.Credentials.from_service_account_info(authFile,scopes=self.SCOPES)
                self.DRIVE = discovery.build('sheets', self.version, credentials=credentials)
            return True,self.DRIVE
        except:
           raise Exception("Error connecting to Google")

    def getRange(self,fileId,range):
        sheet = self.DRIVE.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=fileId, range=range)
            .execute()
        )
        values = result.get("values", [])
        return values

    def setRange(self,fileId:str,range:str,data:list,mode:str="ROWS"):
        #data = [["valuea1"], ["valuea2"], ["valuea3"]]
        self.DRIVE.spreadsheets().values().append(
        spreadsheetId=fileId,
        range=range,
        body={"majorDimension": mode,"values": data },
        valueInputOption="USER_ENTERED",
        ).execute()

    def clearRange(self,fileId:str,range:str):
        sheet = self.DRIVE.spreadsheets()
        sheet.values().clear(spreadsheetId=fileId, range=range,body={}).execute()

        



#s = SheetsLib()

#s.connectDrive("./app/Config/rpa-financas.json",isServiceAccount=True)

#s.getRange("1177SV3X_Jxnd9VF8-OAYTQkksIG2hSfLTfr6xR4tDxA","Base Pagos!R:R")
#s.getRange("1IJFqOV6xwk8x9rv1g5-QGA1X9-jWHaNxeEL2NcxrcPs","teste!A1:G29")

#data = [["valuea1"], ["valuea2"], ["valuea3"]]
#s.setRange("1IJFqOV6xwk8x9rv1g5-QGA1X9-jWHaNxeEL2NcxrcPs","Página3!B4:B6",data,"ROWS")




a  =1