
import requests
from Libs.selenium import SeleniumLib
from Config import BotConfig,SeleniumConfig,AdminVault,GoogleVault,vlt
from Config.loguru import logger
from Libs.loguru import logger_class
from Libs.selenium import SeleniumLib
from selenium.webdriver.common.by import By

@logger_class()
class AdminLib(SeleniumLib):

    def SETUP(self):
        self.setupSelenium(host=SeleniumConfig.HOST,name=BotConfig.NAME,use_selenoid=SeleniumConfig.USE_SELENOID)

    def LOGIN_ADMIN(self):
        #ABRE PAGINA
        self.open_page("https://admin.svc.sympla.com.br")
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
        #ESPERA BOTAO CONTINUAR
        self.wait_xpath("//span[text()='Continuar']")
        #CONTINUAR
        self.driver.find_elements(By.XPATH,"//span[text()='Continuar']")[0].click()
        #AGUARDA CARREGAR A PAGINA
        self.wait_xpath("//header/a/img[@alt='Sympla']")

    def GET_TOKEN(self):
        if  not AdminVault.TOKEN:
            logger.info("\t\tCONFIGURANDO SELENIUM")
            self.SETUP()
            logger.info("\t\tLOGIN ADMINN")
            self.LOGIN_ADMIN()
            token = self.driver.execute_script('return JSON.parse(localStorage.getItem("credentials"))["access_token"]')
            vlt.setVault(AdminVault.vault_path,{"TOKEN":token})
            AdminVault.TOKEN = token
            self.close()

        # TESTA SE O TOKEN E VALIDO
        headers = {'Authorization': f'Bearer {AdminVault.TOKEN}' }
        req = requests.get("https://moes-tavern.svc.sympla.com.br/users/get-users",headers=headers)
        if req.status_code != 200:
            AdminVault.TOKEN = None
            self.GET_TOKEN()
        

        self.headers = {'Authorization': f'Bearer {AdminVault.TOKEN}','Content-Type': 'application/json'}
