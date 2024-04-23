
import requests
from Libs.selenium import SeleniumLib
from Config import BotConfig,SeleniumConfig,AdminVault,GoogleVault,vlt,IntranetVault
from Config.loguru import logger
from Libs.loguru import logger_class
from Libs.selenium import SeleniumLib
from selenium.webdriver.common.by import By
import inspect

class OutroDebito:
    eventid        = None
    note_external  = None
    credit_account = None
    value          = None
    posting_date   = None
    debit_account  = None
    note_internal  = None
    note_sap       = None
    status         = "C"
    action         = "new"
    eppid          = "32156,32157,32158"
    type           = "CREDIT-OTHER"

    def __init__(self,eventid=None,note_external=None,credit_account=None,value=None,posting_date=None,debit_account=None,note_internal=None,note_sap=None):
        self.eventid        = eventid        
        self.note_external  = note_external  
        self.credit_account = credit_account 
        self.value          = value          
        self.posting_date   = posting_date   
        self.debit_account  = debit_account  
        self.note_internal  = note_internal  
        self.note_sap       = note_sap       


    def encode(self,IntranetObj=None):
        params = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        params_filter = [x for x in params if x[0][-2:] != "__" and x[0][1:2] != "__"]
        return "&".join([f"{x[0].replace('_','-')}={x[1]or''}" for x in params_filter])
    
class LcmReembolso180:
    eventid                  = None
    credit_account_retention = None
    debit_account_retention  = None
    credit_account_tax       = None
    debit_account_tax        = None
    credit_account_other     = None
    debit_account_other      = None
    value_retention_other    = None
    posting_date             = None
    note_external            = None
    note_internal            = None
    note_sap                 = None
    order_num                = None
    status                   = None
    #PREENCHIDOS AUTOMATICAMENTE
    value_retention          = None
    value_retention_sympla   = None
    #DADOS FIXOS
    type                     = "LCM-REFUND-180"
    action                   = "new"
    eppid                    = "32156,32157,32158"

    def __init__(self,eventid=None,credit_account_retention=None,debit_account_retention=None,credit_account_tax=None,debit_account_tax=None,credit_account_other=None,debit_account_other=None,value_retention_other=None,posting_date=None,note_external=None,note_internal=None,note_sap=None,order_num=None,status=None):
        self.eventid                  = eventid
        self.credit_account_retention = credit_account_retention
        self.debit_account_retention  = debit_account_retention
        self.credit_account_tax       = credit_account_tax
        self.debit_account_tax        = debit_account_tax
        self.credit_account_other     = credit_account_other
        self.debit_account_other      = debit_account_other
        self.value_retention_other    = value_retention_other
        self.posting_date             = posting_date
        self.note_external            = note_external
        self.note_internal            = note_internal
        self.note_sap                 = note_sap
        self.order_num                = order_num
        self.status                   = status

    def encode(self,IntranetObj=None):
        #PRENCHE DADOS AUTOMATICOS
        data = IntranetObj.ORDER_VALUE(self.order_num)
        if data["status"] != "ok": raise Exception(f"Evento '{self.order_num}' nao encontrado!")
        self.value_retention = data["organizer_value"]
        self.value_retention_sympla = data["sympla_tax_value"]


        params = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        params_filter = [x for x in params if x[0][-2:] != "__" and x[0][1:2] != "__"]
        return "&".join([f"{x[0].replace('_','-')}={x[1]or''}" for x in params_filter])



@logger_class()
class IntranetLib(SeleniumLib):

    def SETUP(self):
        self.setupSelenium(host=SeleniumConfig.HOST,name=BotConfig.NAME,use_selenoid=SeleniumConfig.USE_SELENOID,browser="Firefox")
    
    def LOGIN(self):
        self.open_page("https://intranet.sympla.com.br")
        #CLICA EM LOGAR COM O GOOGLE
        self.driver.find_elements(By.XPATH,"//span[contains(text(),'login com o Google')]")[0].click()
        #DIGITA EMAIL
        self.driver.find_elements(By.XPATH,"//input[@type='email']")[0].send_keys(GoogleVault.USER)
        #AVANÇAR
        self.driver.find_elements(By.XPATH,"//span[text()='Next']")[0].click()
        #ESPERA INPUT DE SENHA
        self.wait_xpath("//input[@type='password']")
        #DIGITA SENHA
        self.driver.find_elements(By.XPATH,"//input[@type='password']")[0].send_keys(GoogleVault.PASSWORD)
        #AVANÇAR
        self.driver.find_elements(By.XPATH,"//span[text()='Next']")[0].click()
        #AGUARDA CARREGAR A PAGINA 
        self.wait_xpath("//h1[contains(text(),'Back-end Sympla')]")
    
    def GET_COOKIE(self):
        cookies_dict = {}
        for cookie in self.driver.get_cookies():
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict

    def CHECK_COOKIE(self):
        self.cookies = {x:IntranetVault.__dict__[x] for x in dict(IntranetVault.__dict__) if x[-2:] != "__" and x[1:2] != "__"}
        isCookieValido = len(self.cookies.keys()) > 1
        if not isCookieValido:
            logger.info("\t\tCONFIGURANDO SELENIUM")
            self.SETUP()
            logger.info("\t\tLOGIN INTRANET")
            self.LOGIN()
            cookie = self.GET_COOKIE()
            vlt.setVault(IntranetVault.vault_path,cookie)
            self.close()
            self.cookies = cookie

        # TESTA SE O TOKEN E VALIDO
        self.headers = {'X-Requested-With': 'XMLHttpRequest','Content-Type': 'application/x-www-form-urlencoded', }
        req = requests.get("https://intranet.sympla.com.br/backend/admin/eventPaymentPosting",headers=self.headers,cookies=self.cookies)
        if req.status_code != 200:
            self.CHECK_COOKIE()
    
    def EVENT_INFO(self,event_id):
        url = "https://intranet.sympla.com.br/backend/admin/eventPaymentPosting"
        payload = f'action=event-info&eid={event_id}'
        req = requests.post(url,headers=self.headers,cookies=self.cookies,data=payload)
        if req.status_code != 200:
            raise Exception(req.text())

        return req.json()
    
    def ORDER_VALUE(self,order_id):
        url = "https://intranet.sympla.com.br/backend/admin/eventPaymentPosting"
        payload = f'action=order-value&order_num={order_id}'
        req = requests.post(url,headers=self.headers,cookies=self.cookies,data=payload)
        if req.status_code != 200:
            raise Exception(req.text())

        return req.json()
    
    def NOVO_LANCAMENTO(self,lancamento:OutroDebito|LcmReembolso180):
        url = "https://intranet.sympla.com.br/backend/admin/eventPaymentPosting"
        payload = lancamento.encode(self)
        req = requests.post(url,headers=self.headers,cookies=self.cookies,data=payload)
        if req.status_code != 200:
            raise Exception(req.text())
        data = req.json()
        if data["status"] == "error":
            raise ValueError(data["error"])
        

    


# lcto = OutroDebito(
#     eventid        = "2341003",
#     note_external  = "Ret. Sobre receita de antec. Adto DIY",
#     credit_account = 234,
#     value          = "25,03",
#     posting_date   = "03/04/2024",
#     debit_account  = 119
# )

# lcto2 = OutroDebito(
#     eventid        = "2341003",
#     note_external  = "Ret. Sobre juros de taxa de admin. CC.31101008",
#     credit_account = 239,
#     value          = "18,64",
#     posting_date   = "03/04/2024",
#     debit_account  = 119
# )


# lcto3 = LcmReembolso180(
#     eventid                  = "38533",
#     value_retention_other    = card['juros'],
#     posting_date             = "03/04/2024",
#     note_internal            = "Card {card['card_id']}",
#     note_sap                 = "REEMBOLSO > 180 DIAS - {card['n_pedido']}",
#     order_num                = card['n_pedido'],
#     status                   = "P",
#     debit_account_retention  = 119,
#     debit_account_tax        = 118,
#     debit_account_other      = 118,
#     credit_account_retention = 19,
#     credit_account_other     = 19,
#     credit_account_tax       = 19,
# )

   
#i = IntranetLib()
#i.CHECK_COOKIE()
# i.EVENT_INFO(123456)
#i.NOVO_LANCAMENTO(lcto2)


