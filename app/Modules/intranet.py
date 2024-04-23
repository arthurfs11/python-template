

import requests
from Libs.selenium import SeleniumLib
from Config import BotConfig,SeleniumConfig,GoogleVault
from Config.loguru import logger
from Libs.loguru import logger_class
from Libs.selenium import SeleniumLib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from time import sleep
from dateUts import today
from Libs.intranet import IntranetLib,LcmReembolso180

@logger_class()
class Intranet(IntranetLib):


    def INICIA_INTRANET(self):
        logger.info("\tCONFIGURA INTRANET")
        self.CHECK_COOKIE()

