
from Libs.cnab.cnab import *
from Config.default import *
from Config.loguru import *
from Config.settings import *
from Config.vault import *

if os.getenv("MODE","DEV")=="PRD":
    from Config.db import *
    from Config.logger_db import *
# from Secure.ofuscate import my_func


def show_config():
    show_data  = lambda key,val:logger.debug(f'{f"{key}:":<15}{val}')
    #===================== MOSTRA AS CONFIGURACOES ATUAIS DO BOT
    logger.debug((f'=====================CONFIG================'))
    show_data("BOTNAME",   BotConfig.NAME)
    show_data("TIME",      f'{now(fmt="sql+hr")} {locale.getlocale()[0]}')
    show_data("LOCALE",    locale.getlocale()[0])
    show_data("MODE",      os.getenv("MODE","DEV"))
    logger.debug(f'-------')
    show_data("USE_SELENOID", SeleniumConfig.USE_SELENOID)
    logger.debug(f'=====================CONFIG================')