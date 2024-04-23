from dotenv import load_dotenv
import locale
import os
#CARREGA VARIAVEIS DE AMBIENTE
load_dotenv("./_.env",override=False)
#CONFIGURA O IDIOMA
#locale.setlocale(locale.LC_TIME, 'pt_BR')


#CRIA AS PASTAS VAZIAS
if not os.path.isdir("./logs"): os.makedirs("./logs") 
if not os.path.isdir("./output"): os.makedirs("./output") 
