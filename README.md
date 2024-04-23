# Nome do Bot
<img src="https://avatars.githubusercontent.com/u/162132687?s=48&v=4" width="30">

## 1 - Sobre
descricao breve sobre a funcionalidade do bot


## 2 - Tecnologias Utilizadas
As tecnologias utilzadas no processo foram:
- python
    - selenium
    - banco de dados Postgres
- Selenoid

## 3 - Instalação
requer python 3.11 para rodar.
Instale as dependencias usando:

```ssh
pip install -r requirements
```

Em seguida execute o processo com:
```ssh
python app
```

caso programado rode o comando:
```ssh
python scheduller.py
```

## 4 - Ambientes
A mudanca de ambiente é configurada na variavel de ambiente chamada `ENV` que pode ter os valores `PRD` ou `DEV`, as mudaças de ambiante impactam nas respectivas atividades:
- DEV
    - Selenium: é utilizado o browser local na maquina do desenvolvedor
- PRD
    - Selenium: é utilizado a conexão via selenoid

_Para fazer a mudançao de ambiente basta alterar a variável  `ENV` no arquivo `_.env`_

## 5 - Config
 No arquivo `Config/configs_prd.ini` é possível encontar todas as connfiguracoes necessarias para a execução do bot em produção:

- `BOT`: guarda dados sobre o processo
- `SELENIUM`: servidor do selenoid utilizado em produção
### scheduller
Para configurar o scheduller verifique o arquivo `scheduller.py` tem a função de programar o tempo de cada execução.

```py
#PROGRAMANDO A EXECUCÃO
schedule.every(10).seconds.do(lambda:(print_time(),main()))
```


## 6 - Execução em DEV
A execução em modo **DEV** esse modo e ativado de forma automática pelo template, esse template identifica quando estamos rodando no docker e muda a chave para **PRD** basta rodar o codigo naa sua maquia com o comando a baixo.
 
```ssh
python app
```

_verifique o step 4 para saber oque muda quando executado em DEV_

## 7 - Deploy em prd
Este bot deve ser instalado em um container docker utilizando o docker-compose.yml para deploy em produção

```ssh
docker-compose up -d
```

_Obs: não esqueca de configurar o servidor selenoid em Config/configs\_prd.ini_





