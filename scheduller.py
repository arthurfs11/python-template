import sys
sys.path.append("./app")
from app.__main__ import main,logger,show_config
from dateUts import now
import schedule
import time


#MOSTRA AS CONFIGURACOES ATUAIS
show_config()
#FUNCAO PARA MOSTRAR A DATA/HORA DA EXECUCAO
print_time = lambda:logger.info(f"SCHEDULLER -----------> {now(fmt='sql+hr')}")

#PROGRAMANDO A EXECUCÃO
schedule.every(10).hours.do(lambda:(print_time(),main()))


while(1):
    schedule.run_pending()
    time.sleep(10)


    