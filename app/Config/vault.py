from Libs.vault import VaultLib
from Config.settings import VaultConfig
import os


vlt = VaultLib(VaultConfig.HOST,VaultConfig.TOKEN,in_prd=os.getenv("MODE","DEV")=="PRD",dev_ini_file="./app/Config/configs_dev.ini")



@vlt.link("Google/data/svc-risco")
class GoogleVault(): 
    type                        : str
    project_id                  : str    
    private_key_id              : str        
    private_key                 : str    
    client_email                : str        
    client_id                   : str    
    auth_uri                    : str    
    token_uri                   : str    
    auth_provider_x509_cert_url : str                    
    client_x509_cert_url        : str                
    universe_domain             : str

@vlt.link("Pipefy/data/auth")
class PipefyVault(): 
    TOKEN  : str

@vlt.link("Slack/data/auth")
class SlackVault(): 
    TOKEN  : str

@vlt.link("Intranet/data/financas",create_missing=True)
class IntranetVault(): 
    #PREENCHIDO PELO VAULT
    pass

@vlt.link("Admin/data/financas")
class AdminVault(): 
    TOKEN   : str

@vlt.link("Google/data/financas")
class GoogleVault(): 
    USER    : str
    PASSWORD: str

@vlt.link("CNAB/data/Sympla")
class CNABVault(): 
    cnpj        : str
    agencia     : str
    conta       : str
    digito      : str
    razao_social: str
    nome_banco  : str
    endereco    : str
    numero      : str
    cep         : str
    municipio   : str
    UF          : str
    pref        : str

@vlt.link("Procob/data/auth")
class ProcobVault(): 
    TOKEN  : str

@vlt.link("Google/data/imap-validacao-carteira")
class GmailVault(): 
    HOST   : str
    PASS   : str
    PORT   : int
    USER   : str