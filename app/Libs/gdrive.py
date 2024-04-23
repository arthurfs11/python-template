from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaInMemoryUpload
from google.oauth2 import service_account
import os
import mimetypes

class DriveLib:
    DRIVE = None
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    version = "v3"
    
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
                self.DRIVE = discovery.build('drive', self.version, credentials=credentials)
            return self.DRIVE
        except:
           raise Exception("Error connecting to Google")

    def runQuery(self,query):
        files2 = []
        page_token = None
        while True:
            files = self.DRIVE.files().list( q=query,
                                        fields='nextPageToken, files(id, name, parents)',
                                        pageToken=page_token,
                                        supportsAllDrives = True,
                                        includeItemsFromAllDrives = True
                                        ).execute()
            page_token = files.get('nextPageToken', None)

            files2.extend(files.get('files', []))

            if page_token is None:
                break
        return files2

    def getFile(self,FileId,fields="id, name, parents, mimeType"):
            return self.DRIVE.files().get(fileId=FileId,fields=fields).execute() 

    def downloadFile(self,FileId,to):
        fl = self.getFile(FileId)

        file_content = self.DRIVE.files().get_media(fileId=FileId).execute()
        fl = os.path.join(to, fl["name"])
        with open(fl, 'wb') as f:
            f.write(file_content)

    def getAllFiles(self,folderId=None):
        query = "" if folderId == None else ("'" + folderId + "' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'")
        return self.runQuery(query)


    def getAllFolders(self,folderId=None):
        query = "" if folderId == None else ("'" + folderId + "' in parents and ")
        query += "mimeType = 'application/vnd.google-apps.folder' and trashed=false"
        return self.runQuery(query)

    def findFile(self,fileName,folderId=None,isFile=True,operator="="):
        #operator '=' or 'contains' or'!='
        query = "" if folderId == None else ("'" + folderId + "' in parents and ")
        query += "mimeType " + ("!=" if isFile else "=") +" 'application/vnd.google-apps.folder' and "
        query += "name " + operator + "'" + fileName + "' and trashed=false"
        #print(query)
        return self.runQuery(query)

    def createFolder(self,FolderName,folderId=None):
        if "/" in FolderName or "\\" in FolderName:
            current = FolderName.replace("\\","/").split("/")[0]
            nxt = FolderName.replace("\\","/").split("/")[1]
        else:
            current = FolderName
            nxt = None

        file_metadata = {
            'name': current,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if folderId != None:
            file_metadata["parents"]=[folderId]

        file = self.DRIVE.files().create(body=file_metadata,fields='id, name, parents',supportsAllDrives = True).execute()
        
        if nxt: return self.createFolder(nxt,file["id"])
        return file

    def GetAllFilesChildren(self,FolderID):
        Files = []
        f = self.getAllFiles(FolderID)
        Files.extend(f)

        Folders = self.getAllFolders(FolderID)

        for fdr in Folders:
            t = self.GetAllFilesChildren(fdr["id"])
            Files.extend(t)
        return Files

    def CopyFile(self,FileId,ToFolderId=None,NewName=None):
        copied_file = {}
        if ToFolderId != None:
            copied_file["parents"] = [ToFolderId]
        if NewName != None:
            copied_file["name"] = [NewName]   
        return True,self.DRIVE.files().copy(fileId=FileId, body=copied_file,fields='id, name, parents').execute()

    def CopyFolder(self,FromFolderId,ToFolderID):
        OldFolder = self.getFile(FromFolderId)

        NewFoder = self.createFolder(OldFolder["name"],ToFolderID)
        
        files = self.getAllFiles(FromFolderId)

        for f in files:
            self.CopyFile(f["id"],NewFoder["id"])

        Folders = self.getAllFolders(FromFolderId)

        for fdr in Folders:
            self.CopyFolder(fdr["id"],NewFoder["id"])
        return ""

    def checkAndCreateFolder(self,Foldername,folderId="root"):
        Foldername = Foldername.replace("/","\\")
        Foldername = Foldername if Foldername[-1:] != "\\" else Foldername[:-1]
        Foldername = Foldername.split("\\")

        lastFolder = {"id":folderId}
        for fdr in Foldername:
            PASTA = self.findFile(fdr,lastFolder["id"],False)

            if len(PASTA) > 0:
                lastFolder = PASTA[0]
            else:
                lastFolder = self.createFolder(fdr,lastFolder["id"])
        
        return lastFolder

    def getUploadProgress(self,file):
        #response = None
        status, response = file.next_chunk()
        #while response is None:
        if response is None:
            #status, response = file.next_chunk()
            return "{0:.2f}".format(round((status.progress() * 100),2))
        else:
            return None
            #print(status.progress())
            #if status:
                #print ("Uploaded %d%%." % int(status.progress() * 100))

        #if not file:
        #    return False,"File not uploaded"

    def uploadFile(self,Fileaddr,folderId=None,resume=False):
        file_metadata = {
            'name': os.path.basename(Fileaddr),
            'parents': []
        }   
        if folderId != None:
            file_metadata["parents"]=[folderId]

        mimetyp = mimetypes.guess_type(Fileaddr)[0]
        #print(Fileaddr)
        media = MediaFileUpload(Fileaddr,mimetype=mimetyp,chunksize=256 * 1024,resumable=True)

        file = self.DRIVE.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, parents',
            supportsAllDrives = True
            )
        if not resume:
            file.execute()
        #.execute()
        #file = self.DRIVE.files().insert(body=file_metadata,media_body=media,fields='id, alternateLink')

        #print ("Your sharable link: "+ "https://drive.google.com/file/d/" + response.get('id')+'/view')

        return file
            

    def uploadFileMem(self,File,folderId=None,resume=False,tries=1):
        try:
            file_metadata = {
                'name': File["name"],
                'parents': []
            }   
            if folderId != None:
                file_metadata["parents"]=[folderId]

            mimetyp = File["content_type"]
            #print(Fileaddr)
            media = MediaInMemoryUpload(File["stream"],mimetype=mimetyp,chunksize=256 * 1024,resumable=True)

            file = self.DRIVE.files().create(body=file_metadata,media_body=media,fields='id, name, parents')
            if not resume:
                file.execute()
            #.execute()
            #file = self.DRIVE.files().insert(body=file_metadata,media_body=media,fields='id, alternateLink')

            #print ("Your sharable link: "+ "https://drive.google.com/file/d/" + response.get('id')+'/view')

            return True,file
        except:
            if tries>1: 
                print("===============PASSOU=============")
                return self.uploadFileMem(File,folderId,resume,tries-1)
            #print(traceback.format_exc() )
            raise

    def deleteFile(self, file_id):
        body = {'trashed': True}
        self.DRIVE.files().update(
            fileId=file_id, 
            body=body,
            supportsAllDrives = True
            ).execute()
        # self.DRIVE.files().delete(
        #     fileId=file_id,
        #     supportsAllDrives = True
        #     ).execute()

#d = DriveLib()

#d.connectDrive()

#fls = d.getAllFiles()  # demora pq  vai pegar todo os arquivos do drive

#d.downloadFile("1G5efvgWPT6QW7Xlr_ZA9OVAhUTP11qiY","")

#a =1