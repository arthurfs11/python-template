import os
from iniUts import *
from dateUts import now
from Config.loguru import logger


#===================== POPULA AS CLASSES DE CONFIGURACAO 
ini =  IniUts("./app/Config/configs_prd.ini","./app/Config/configs_dev.ini",in_prd=os.getenv("MODE","DEV")=="PRD")

@ini.link("BOT")
class BotConfig(): 
    NAME    : str

@ini.link("SELENIUM")
class SeleniumConfig(): 
    HOST         :str
    USE_SELENOID : bool

@ini.link("DB")
class DbConfig(): 
    SERVER  : str
    USER    : str
    PWD     : str

@ini.link("VAULT")
class VaultConfig(): 
    HOST  : str
    TOKEN  : str