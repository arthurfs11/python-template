from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import platform


class SlackLib:
    client=None
    
    def __init__(self,token):
        self.client = WebClient(token)
    
    def sendMessage(self,channel,message):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            raise Exception(e.response["error"])
    
    def sendTextFileFromString(self,channel,title,message,file_name,text_file_content):
        #ENVIO PRECISA SER FEITO COM \r\n PELA API
        text = text_file_content if "\r\n" in text_file_content else text_file_content.replace("\n","\r\n")
        self.client.files_upload_v2(
            channel=channel,
            title=title,
            filename=file_name,
            content=text,
            initial_comment=message,
        )

    def sendFile(self,channel,title,message,file_addr):
        self.client.files_upload_v2(
            channel=channel,
            title=title,
            file=file_addr,
            initial_comment=message,
        )
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import platform


class SlackLib:
    client=None
    
    def __init__(self,token):
        self.client = WebClient(token)
    
    def sendMessage(self,channel,message):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            raise Exception(e.response["error"])
    
    def sendTextFileFromString(self,channel,title,message,file_name,text_file_content):
        #ENVIO PRECISA SER FEITO COM \r\n PELA API
        text = text_file_content if "\r\n" in text_file_content else text_file_content.replace("\n","\r\n")
        self.client.files_upload_v2(
            channel=channel,
            title=title,
            filename=file_name,
            content=text,
            initial_comment=message,
        )

    def sendFile(self,channel,title,message,file_addr):
        self.client.files_upload_v2(
            channel=channel,
            title=title,
            file=file_addr,
            initial_comment=message,
        )
