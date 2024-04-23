import json
from dateUts import now
import platform
from unicodedata import normalize
from functools import partial
import fitz
from datetime import datetime as dt
from Libs.cnab.pdf_positions import PDF_FIELDS
from Libs.cnab.pagamentos import FORMA_PAGAMENTOS
from Libs.cnab.bancos import BANCOS_DICT

class CnabCreateLib:
    default = None
    def __init__(self,default_file:str=None,default_info:dict=None):
        self.default = json.load(open(default_file)) if default_file else default_info
    
    def primeira_linha(self):
        return "".join([
            "341",                                                              #CÓDIGO DO BANCO
            "0000",                                                             #CÓDIGO DO LOTE
            "0",                                                                #TIPO REGISTRO
            " "*6,                                                              #BRANCOS
            "080",                                                              #LAYOUT DE ARQUIVO
            "2",                                                                #E O TIPO DO DOCUMENTO VALIDAR SE VAI SER SEMPRE 2- CNPJ OU MUDA PRA CPF
            "".join([x for x in self.default["cnpj"] if x in "0123456789"]),    #CNPJ EMPRESA DEBITADA (14)
            " "*20 ,                                                            #BRANCOS
            self.default["agencia"].zfill(5),                                   #AGENCIA
            " " +                                                               #BRANCOS
            self.default["conta"].zfill(12) ,                                   #CONTA DEBITADA
            " " ,                                                               #BRANCOS
            self.default["digito"],                                             #DIGITO
            self.default["razao_social"].ljust(30)[:30] ,                       #NOME DA EMPRESA
            self.default["nome_banco"].ljust(30)[:30] ,                         #NOME DO BANCO
            " "*10,                                                             #BRANCOS
            "1",                                                                #REMESSA
            now(fmt='%d%m%Y%H%M%S'),                                          #DATA HORA
            "0"*9,                                                              #ZEROS
            "0"*5,                                                              #UNIDADE DE DENSIDADE
            " "*69                                                              #BRANCOS
        ])

    def segunda_linha(self,mode:str):
        mode = "41" if mode == "TED" else "01"
        return "".join([
            "341",                                                              #CÓDIGO DO BANCO
            "0001",                                                             #LOTE
            "1",                                                                #TIPO DE REGISTRO
            "C",                                                                #TIPO OPERACAO
            "20",                                                               #TIPO DE PAGAMENTO
            mode,                                                               #FORMA DE PAGAMENTO
            "040",                                                              #LAYOUT DO LOTE
            " ",                                                                #BRANCO
            "2",                                                                #EMPRESA – INSCRIÇÃO
            "".join([x for x in self.default["cnpj"] if x in "0123456789"]),           #CNPJ (14)
            " "*4,                                                              #IDENTIFICAÇÃO DO LANÇAMENTO
            " "*16,                                                             #BRANCOS
            self.default["agencia"].zfill(5),                                   #AGENCIA
            " " +                                                               #BRANCOS
            self.default["conta"].zfill(12) ,                                   #CONTA DEBITADA
            " " ,                                                               #BRANCOS
            self.default["digito"],                                             #DIGITO
            self.default["razao_social"].ljust(30)[:30] ,                       #NOME DA EMPRESA
            " "*30,                                                             #FINALIDADE LOTE
            " "*10,                                                             #HISTÓRICO DE C/C
            self.default["endereco"].ljust(30)[:30],                                   #ENDEREÇO DA EMPRESA
            self.default["numero"].zfill(5),                                           #NÚMERO
            " "*15,                                                             #COMPEMENTO
            self.default["municipio"].ljust(20)[:20],                                  #CIDADE
            "".join([x for x in self.default["cep"] if x in "0123456789"]),            #CEP
            self.default["UF"],                                                        #ESTADO
            " "*8,                                                              #BRANCOS    
            " "*10                                                              #BRANCOS    
            ])

    def registro_pag(self,n_registro,cd_banco,agencia,conta,digito,nome,seu_numero,valor,documento):
        return "".join([
            "341",                                                              #CÓDIGO DO BANCO
            "0001",                                                             #CÓDIGO DO LOTE
            "3",                                                                #TIPO REGISTRO
            str(n_registro).zfill(5),                                                #NÚMERO DO REGISTRO
            "A",                                                                #SEGMENTO
            "000",                                                              #TIPO DE MOVIMENTO
            "000",                                                              #CÂMARA
            cd_banco.zfill(3),                                                  #CÓDIGO BANCO FAVORECIDO (3)
            agencia.zfill(5),                                                   #AGENCIA FAVORECIDO(5)
            " ",                                                                #BRANCO
            conta.zfill(12),                                                    #CONTA FAVORRECIDO (12)
            " ",                                                                #BRANCO
            digito,                                                             #DIGITOCONTA FAVORECIDO
            self.retira_acentos(nome).ljust(30)[:30],                           #NOME DO FAVORECIDO
            seu_numero.ljust(20)[:20],                                          #SEU NÚMERO
            now(fmt='%d%m%Y'),                                                  #DATA PAGAMENTO
            "REA",                                                              #MOEDA – TIPO
            "0"*8,                                                              #CÓDIGO ISPB
            "0"*2,                                                              #IDENTI. TRANSFERENCIA
            "0"*5,                                                              #ZEROS
            str(int(valor)).zfill(13),                                          #VALOR DO PAGTO
            format(valor, '.2f').split('.')[1],                                 #CENTAVOS
            " "*15,                                                             #NOSSO NÚMERO
            " "*5,                                                              #BRANCOS
            "0"*8,                                                              #DATA EFETIVA
            "0"*15,                                                             #VALOR EFETIVO
            " "*20,                                                             #FINALIDADE DETALHE 
            "0"*6,                                                              #N DO DOCUMENTO 
            "".join([x for x in documento if x in "0123456789"]).ljust(14)[:14],#N DE INSCRIÇÃO 
            " "*2,                                                              #FINALIDADE DOC E STATUS FUNCIONÁRIO 
            " "*5,                                                              #FINALIDADE TED 
            " "*5,                                                              #BRANCOS
            "5",                                                                #AVISO
            " "*10                                                             #OCORRÊNCIAS
        ])

    def rodape_primeira_linha(self,qtd_registros,total):
        return "".join([
            "341",                                                              #CÓDIGO DO BANCO
            "0001",                                                             #CÓDIGO DO LOTE
            "5",                                                                #TIPO REGISTRO
            " "*9,                                                              #BRANCO
            str(qtd_registros+2).zfill(6),                                         #NÚMERO DO REGISTRO
            str(int(total)).zfill(16),                                          #VALOR DO PAGTO
            format(total, '.2f').split('.')[1],                                 #CENTAVOS
            "0"*18,                                                             #ZEROS
            " "*171,                                                            #BRANCO
            " "*10                                                              #BRANCO
        ])

    def rodape_segunda_linha(self,qtd_registros):
        return "".join([
            "341",                                                              #CÓDIGO DO BANCO
            "9999",                                                             #CÓDIGO DO LOTE
            "9",                                                                #TIPO REGISTRO
            " "*9,                                                              #TIPO DE OPERAÇÃO
            "000001",                                                           #TOTAL QTDE DE LOTES
            str(qtd_registros+4).zfill(6),                                      #NÚMERO DO REGISTROS
            " "*211                                                             #BRANCO
        ])
    
    def valida_trans(self,trans):
        campos = ["cd_banco","agencia","conta","digito","nome","seu_numero"]

        #VALIDA CAMPOS EXISTENTES
        for t in trans:
            if set(campos).difference(set(t.keys())):
                faltantes = set(campos).difference(set(t.keys()))
                raise Exception(f"campos nao encontrados: {faltantes}")
        
        #VALIDA VALORES
        for t in trans:
            if len(t["agencia"]) > 5 or len(t["agencia"])==0:
                raise Exception("campo agencia invalido!")
            if len(t["cd_banco"]) > 3 or len(t["cd_banco"]) == 0:
                raise Exception("campo cd_banco invalido!")
            if len(t["conta"]) > 12 or len(t["conta"]) == 0:
                raise Exception("campo conta invalido!")
            if len(t["digito"]) != 1:
                raise Exception("campo digito invalido!")
            if len(t["nome"]) == 0:
                raise Exception("campo nome invalido!")
            if len(t["seu_numero"]) > 20 or len(t["seu_numero"]) == 0:
                raise Exception("campo seu_numero invalido!")


    def retira_acentos(self,text):
        return normalize('NFKD', text).encode('ASCII','ignore').decode('ASCII')

    def gera_cnab(self,trans,mode):

        total = sum([x["valor"] for x in trans])
        self.valida_trans(trans)

        linhas = [
            self.primeira_linha(),
            self.segunda_linha(mode), #TED ou TRANSF
            *[self.registro_pag(y,**x) for x,y in zip(trans,range(1,len(trans)+1))],
            self.rodape_primeira_linha(len(trans),total),
            self.rodape_segunda_linha(len(trans))
        ]

        char = "\n" if "Windows" in platform.platform() else "\r\n"

        cnab = char.join(linhas)+char

        return cnab    


class Transacao:
    def __init__(self,linhas,main_lote,main_cnab,forma_pagamento):
        self.linhas = linhas
        self.forma_pagamento = forma_pagamento
        self._main_lote = main_lote
        self._main_cnab = main_cnab
    
    def __repr__(self) -> str:
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
 
        return f"<Transacao {getValue(self.linhas[0],9,5)}>"


    def nota_11(self,linha):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        getValue = partial(getValue,linha)
        
        cd_banco = getValue(1,3)
        if cd_banco in ['341','409']:
            return {
                "agencia_favorecido":getValue(25,4),
                "conta_favorecido":getValue(36,6),
                "digito_favorecido":getValue(43,1),
            }
        else:
            raise Exception("codigo do banco inválido")

    def segmentos(self):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        segmentos = [getValue(x,14,1) for x in self.linhas]
        return segmentos

    def seg_a(self):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        linha = [x for x in self.linhas if getValue(x,14,1) == 'A']
        if not linha: return None
        
        getValue = partial(getValue,linha[0])

        if self.forma_pagamento in ['10','03','07','41','43','45','47']: 

            return {
                "cd_banco":getValue(1,3),
                "cd_lote":getValue(4,4),
                "tipo_reg":getValue(8,1),
                "numero_reg":getValue(9,5),
                "segmento":getValue(14,1),
                "tipo_movimento":getValue(15,3),
                "banco":getValue(21,3),
                **self.nota_11(linha[0]),
                "nome_favorecido":getValue(44,30),
                "seu_numero":getValue(74,20),
                "data_pagamento":getValue(94,8),
                "tipo_moeda":getValue(102,3),
                "valor":int(getValue(120,13)) + int(getValue(133,2))/100,
                "nosso_numero":getValue(135,15),
                "data_efetiva":getValue(155,8),
                "valor_efetivo":int(getValue(163,13)) + int(getValue(176,2))/100,
                "nota_fiscal_cnpj":getValue(178,15),
                "documento":getValue(198,6),
                "numero_inscricao":getValue(204,14),
                "tipo_edentificacao":getValue(218,1),
                "aviso":getValue(230,1),
                "ocorrencias":getValue(231,10),
            }
        else:
            raise Exception(f"forma pagamento '{self.forma_pagamento}' nao mapeada")

    def seg_z(self):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        linha = [x for x in self.linhas if getValue(x,14,1) == 'Z']
        if not linha: return None
        
        getValue = partial(getValue,linha[0])

        if self.forma_pagamento in ['02','06','10','03','07','43']: 

            return {
                "cd_banco":getValue(1,3),
                "cd_lote":getValue(4,4),
                "tipo_registro":getValue(8,1),
                "quantidade_registros":getValue(18,6),
                "valor_total":getValue(24,18),
                "ocorrencias":getValue(231,10),
            }
        elif self.forma_pagamento in ['30','31','41','45','47','91']: 

            return {
                "cd_banco":getValue(1,3),
                "cd_lote":getValue(4,4),
                "tipo_registro":getValue(8,1),
                "numero_registro":getValue(9,5),
                "codigo_segmento":getValue(14,1),
                "autenticacao":getValue(15,64),
                "seu_numero":getValue(79,20),
                "nosso_numero":getValue(104,15),
            }
        
        else:
            raise Exception(f"forma pagamento '{self.forma_pagamento}' nao mapeada")

    def seg_j(self):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        linha = [x for x in self.linhas if getValue(x,14,1) == 'J']
        if not linha: return None
        
        getValue = partial(getValue,linha[0])

        if self.forma_pagamento in ['31','47']: 

            return {
                "cd_banco":getValue(1,3),
                "cd_lote":getValue(4,4),
                "tipo_registro":getValue(8,1),
                "numero_registro":getValue(9,5),
                "segmento":getValue(14,1),
                "tipo_movmento":getValue(15,3),
                "banco_favorecido":getValue(18,20),
                "moeda":getValue(21,1),
                "dv":getValue(22,1),
                "vencimento":getValue(23,4),
                "valor":getValue(27,10),
                "campo_livre":getValue(37,25),
                "nome_favorecido":getValue(62,30),
                "vencimento":getValue(92,8),
                "valor_titulo":getValue(100,15),
                "descontos":getValue(15,15),
                "accrecimos":getValue(130,15),
                "data":getValue(145,8),
                "vaor_pagamento":getValue(153,167),
                "seu_numero":getValue(183,20),
                "nosso_numero":getValue(213,15),
                "ocorrencias":getValue(231,10)
            }
        elif self.forma_pagamento in ['30','31','41','45','47','91']: 

            return {
                "cd_banco":getValue(1,3),
                "cd_lote":getValue(4,4),
                "tipo_registro":getValue(8,1),
                "numero_registro":getValue(9,5),
                "codigo_segmento":getValue(14,1),
                "autenticacao":getValue(15,64),
                "seu_numero":getValue(79,20),
                "nosso_numero":getValue(104,15),
            }
        
        else:
            raise Exception(f"forma pagamento '{self.forma_pagamento}' nao mapeada")

    def gera_comprovante(self,output):
        if not 'Z' in self.segmentos(): raise Exception("Transação nao contem o segmento 'Z'")
        if not 'A' in self.segmentos():  raise Exception("Segmento inválido")
        data_header = self._main_cnab.header()
        seg_a = self.seg_a()
        seg_z = self.seg_z()
        date = dt.strptime(data_header["data_hora"],'%d%m%Y%H%M%S').strftime("%d.%m.%Y as %H:%M:%S")
        bank_data = BANCOS_DICT.get(data_header["cd_banco"])
        if not bank_data: raise Exception(f"banco '{data_header['cd_banco']}' nao cadastrado!")
        DATA = {
            "FORMA_PGTO": FORMA_PAGAMENTOS[self.forma_pagamento],
            "IDENT": "<IDENT>",
            "AG": data_header["agencia"],
            "ACC": f'{data_header["agencia"]} - {data_header["digito"]}',
            "NAME1": data_header["nome_empresa"],
            "NAME2": seg_a["nome_favorecido"],
            "BANKCODE_BANKNAME_BANKISPB": f'{seg_a["cd_banco"]} - {bank_data["name"]} - ISPB {bank_data["ispb"]} ',
            "AG2": seg_a["agencia_favorecido"],
            "CC": seg_a["conta_favorecido"],
            "DOC": seg_a["numero_inscricao"],
            "VAL": 'R$ ' + '{:20_.2f}'.format(seg_a["valor"]).replace(".",",").replace("_",".").strip(),
            "FIN": "CREDITO EM CONTA",
            "DETALHES":f"Transferência realizada em {date}, CTRL {seg_a['seu_numero']}",
            "AUTH": seg_z["autenticacao"],
        }

        doc = fitz.open(f"./app/Libs/cnab/template.pdf")
        doc[0].insert_font(fontfile="arial-mt.ttf", fontname="NORMAL")
        doc[0].insert_font(fontfile="arial-mt-bold.ttf", fontname="BOLD")

        for pos in PDF_FIELDS:
            point = fitz.Point(PDF_FIELDS[pos][0],PDF_FIELDS[pos][1])    
            doc[0].insert_text(point - (0,3), DATA[pos],fontsize = 9.9671, color=(0.2, 0.2, 0.2),fontname=PDF_FIELDS[pos][2])
        
        doc.save(output)



class Lote:
    def __init__(self,main_cnab,linhas):
        self.linhas = linhas
        self._main_cnab = main_cnab

    def __repr__(self) -> str:
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
 
        return f"<Lote {getValue(self.linhas[0],4,4)}>"

    def header(self):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        getValue = partial(getValue,self.linhas[0])

        return {
            "cd_banco":getValue(1,3),
            "cd_lote":getValue(4,4),
            "tipo_reg":getValue(8,1),
            "tipo_operacao":getValue(9,1),
            "tipo_pagamento":getValue(10,2),
            "forma_pagamento":getValue(12,2),
            "layout":getValue(14,3),
            "tipo_doc":getValue(18,1),
            "doc":getValue(19,14),
            "identificacao_lancamento":getValue(33,4),
            "agencia":getValue(53,5),
            "conta":getValue(59,12),
            "digito":getValue(72,1),
            "nome_empresa":getValue(73,30),
            "finalidade_lote":getValue(103,30),
            "historico_cc":getValue(133,10),
            "endereco_empresa":getValue(143,30),
            "numero":getValue(173,5),
            "complemento":getValue(178,15),
            "cidade":getValue(193,20),
            "cep":getValue(213,8),
            "estado":getValue(221,2),
            "ocorrencias":getValue(231,10)
        }
    
    def transacoes(self):
        transacoes = {}
        for linha in self.linhas:
            getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
            tipo_registro = getValue(linha,8,1)

            if tipo_registro != '3': continue

            codigo_transacao = getValue(linha,9,5)

            if codigo_transacao not in transacoes: transacoes[codigo_transacao] = []
            
            transacoes[codigo_transacao].append(linha)
        return [Transacao(x,main_cnab=self._main_cnab,main_lote=self,forma_pagamento=getValue(self.linhas[0],12,2)) for x in transacoes.values()]


class CnabReadLib:

    def __init__(self,cnab_text):
        self.cnab = cnab_text
    
    def pega_linha(self,linha):
        text_linha = self.cnab.split("\n")[linha]
        if len(text_linha) != 240:
            raise Exception("Numero de caracteres inválido")
        return text_linha.strip()

    def header(self):
        getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
        linha = self.pega_linha(0)

        getValue = partial(getValue,linha)

        return {
            "cd_banco":getValue(1,3),
            "cd_lote":getValue(4,4),
            "tipo_reg":getValue(8,1),
            "layout":getValue(15,3),
            "tipo_doc":getValue(18,1),
            "documento":getValue(19,14),
            "agencia":getValue(53,5),
            "conta":getValue(59,12),
            "digito":getValue(72,1),
            "nome_empresa":getValue(73,30),
            "nome_banco":getValue(103,30),
            "codigo_arquivo":getValue(143,1),
            "data_hora":getValue(144,14),
            "unidade_densidade":getValue(167,5)
        }

    def lotes(self):
        lotes = {}
        total_linhas = len(self.cnab.split("\n"))
        for l in range(0,total_linhas-1):
            linha = self.pega_linha(l)
            getValue = lambda row,x,tam:row[x-1:x-1+tam].strip()
            codigo_lote = getValue(linha,4,4)

            if codigo_lote in ['0000','9999']: continue
            if codigo_lote not in lotes: lotes[codigo_lote] = []
            5
            lotes[codigo_lote].append(linha)


            pass
        return [Lote(main_cnab=self,linhas=x) for x in lotes.values()]

            

cnb = CnabReadLib(open(r"C:\Users\melquisedeque.lima_s\Documents\R_I2F110424001.txt",'r').read())

cnb.header()
cnb.lotes()[0].header()

#cnb.lotes()[0].transacoes()[0].seg_a()
cnb.lotes()[0].transacoes()[1].gera_comprovante(r"C:\Users\melquisedeque.lima_s\Documents\teste.pdf")
cnb.lotes()[0].transacoes()[0].gera_comprovante("./teste.pdf")

pass
# cnb = CNABLib('default.json')


# cnb.gera_cnab(json.load(open('teste.json')))














