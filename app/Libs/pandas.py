import pandas as pd
import unicodedata

class PandasLib:
    
    
    def ajusta_titulos(df:pd.DataFrame):
        '''
            Essa função faz:
                espaços para _
                retira espaços extras
                retira acentuacao
        '''
        df_loc = df.copy()

        retira_acentuacao  = lambda titulo:unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode("ascii")
        para_minusculas    = lambda titulo:titulo.lower() 
        retira_espacos_ext = lambda titulo: titulo.replace("  "," ")
        retira_laterais    = lambda titulo: titulo.strip()
        retira_espacos     = lambda titulo: titulo.replace(" ","_")
        df_loc.columns = df_loc.columns.map(retira_acentuacao)
        df_loc.columns = df_loc.columns.map(para_minusculas)
        df_loc.columns = df_loc.columns.map(retira_espacos_ext)
        df_loc.columns = df_loc.columns.map(retira_laterais)
        df_loc.columns = df_loc.columns.map(retira_espacos)

        return df_loc
        
