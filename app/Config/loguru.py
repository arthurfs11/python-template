from loguru import logger
from dateUts import now
import platform
import json
import sys
import os

#===================== LIMPA O TERMINAL DE COMANDO
os.system("cls" if "Windows" in platform.platform() else "clear")


#====================== MARCA QUANDO A EXECUCAO TEVE WARNING
HAS_WARNING, HAS_ERROR = False,False
def warning_error(record):
    global HAS_WARNING
    global HAS_ERROR
    data = json.loads(record)["record"]
    if data["level"]['name'] == 'WARNING':
        HAS_WARNING = True
    else:
        HAS_ERROR = True

#====================== AJUSTE DE NOME DE ARQUIVO DOS LOGS
def rename_rotated_file(filepath):
    new_path = os.path.dirname(filepath) + f"/{now(fmt='%Y-%m-%d_T_%H-%M-%S')}.log"
    os.rename(filepath, new_path)

#====================== AJUSTE DE QUEBRA DE LINHA DO LOG
def flatten_message(record):
        record["message"] = record["message"].replace("\n", " ").replace("{","{{").replace("}","}}")
logger = logger.patch(flatten_message)
#===================== REMOVE OS HANDLERS PADROES DO LOGURU
logger.remove()

#===================== HANDLER DE ARQUIVO - GERA UM ARQUIVO POR DIA
logger.add(
    "logs/current.log", 
    format="{time:YYYY-MM-DD at HH:mm:ss} | {file: ^20} | {function: ^15} | {line: ^4} | {extra[file_name]: ^20} | {extra[func_name]: ^15} | {extra[line_exec]: ^4} | {level: ^8} | {message}",
    #format="{extra[line]}",
    rotation='00:00:00',
    serialize=False, 
    encoding='utf-8',
    compression=rename_rotated_file
    )
#===================== HANDLER DO TERMINAL DE COMANDO
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level: ^8}</level> | {file: ^20} | {function: ^15} | {line: ^4} | {extra[file_name]: ^20} | {extra[func_name]: ^15} | {extra[line_exec]: ^4} | <level>{message}</level>",
    backtrace=True,
    diagnose=True
)



#===================== HANDLER DO WARNING/ERROR
logger.add(
    warning_error,
    serialize=True,
    filter=lambda r:r["level"].name in ["WARNING","ERROR"]
)

#===================== HABILITA AS CORES NO TERMINAL
logger.opt(colors=True)

#=====================  CONFIGURACAO DA FORMATAÇÃO DAS MENSAGENS
logger = logger.bind(line_exec="",func_name="",file_name="",time_exec="")

open("./logs/current.log","a").write(f"#{'='*200}\n")