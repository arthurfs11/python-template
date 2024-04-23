import requests
from Libs.selenium import SeleniumLib
from Config import BotConfig,ini,AdminVault
from Config.loguru import logger
from Libs.loguru import logger_class
from Libs.selenium import SeleniumLib
from dateUts import *
from datetime import datetime as dt

from Libs.admin import AdminLib

@logger_class()
class Admin(AdminLib):


    # ORQUESTRADOR
    def DADOS_ADMIN(self):
        logger.info("\tGET_TOKEN")
        self.GET_TOKEN()