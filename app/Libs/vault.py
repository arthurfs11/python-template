import configparser as cp
import requests
import json

class VaultLib:
    def __init__(self,host,token:str,in_prd:bool,dev_ini_file=None):
        self.token = token
        self.host = host
        self.in_prd = in_prd
        self.dev_ini_file = dev_ini_file
    
    def getVault(self,path):
        url = f"{self.host}/v1/{path}"

        headers = {'X-Vault-Token': self.token}

        response = requests.request("GET", url, headers=headers, data={})
        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()['data']['data']

    def Section2Dict(self,section,fileIni,empty_as_null=False):
        config = cp.RawConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(fileIni)

        dc = dict(config[section])
        return dc if not empty_as_null else {x:(y or None) for x,y in dc.items()}

    def vault2DataClass(self,path,dtClass,skip_missing=False,create_missing=False,dev_section=None):
        vault = self.getVault(path)
        dt_dev = self.Section2Dict(dev_section,fileIni=self.dev_ini_file) if dev_section else None
        dtClass.vault_path = path
        for k, v in vault.items():
            if not k in dtClass.__annotations__:
                if not create_missing and not create_missing:
                    raise Exception(f"please create the key '{k}' in data class object")
                elif create_missing:
                    setattr(dtClass, k, v)
                else:
                    continue
            setattr(dtClass, k, v)

        if not self.in_prd and dev_section:
            for k, v in dt_dev.items():
                if not k in dtClass.__annotations__:
                    raise Exception(f"key '{k}' not found in data class object")
                setattr(dtClass, k, v)
        
    def link(self,path,skip_missing=False,create_missing=False,dev_section=None):
        def wrap(function):
            self.vault2DataClass(path,function,skip_missing,create_missing,dev_section)
            return function
        return wrap

    def setVault(self,path,data):
        url = f"{self.host}/v1/{path}"

        headers = {'X-Vault-Token': self.token,'Content-Type':'application/json'}

        data2 = {"data": data}

        response = requests.request("POST", url, headers=headers, data=json.dumps(data2))
        if response.status_code != 200:
            raise Exception(response.text)
