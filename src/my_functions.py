import pandas as pd
import seaborn as sns



"""
Sobre   : Função responsável por retirar as linhas 
          que não possuem as informações mínimas. São
          consideradas lixo.

Entradas: input_columns:
            Colunas que são consideradas como obri-
            gatórias para a amostra não ser conside-
            rada como lixo.
          input_dataframe:
            Dataframe de entrada

saída   : Dataframe 

"""
def remove_trash(input_columns, input_dataframe):
    return input_dataframe.dropna(subset= input_columns,how='all')

"""
Sobre   : Função responsável por retirar as linhas 
          que estão duplicadas

Entradas: input_columns:
            lista 
          input_dataframe:
            Dataframe de entrada

saída   : Dataframe 

"""
def remove_duplicates_rows(input_columns, input_dataframe):
    return input_dataframe.drop_duplicates(subset= input_columns)

"""
Sobre   : Função responsável por cirar um dataframe 
          que vai conter um calendário contínuo em
          relação a data do chamado.

Entradas: data_series:
            series contendo as datas 

saída   : Dataframe contendo as novas datas

"""
def creat_master_Calendar(series_date):
    date_interval = pd.to_datetime(series_date,format="%Y/%m/%d")
    mc = pd.DataFrame({"date_aux": pd.date_range(date_interval.min(), date_interval.max())})
    mc["year"]     = mc.date_aux.dt.year
    mc["month"]    = mc.date_aux.dt.month
    mc["month_name"]    = mc.date_aux.dt.month_name(locale='pt_BR.UTF-8')
    mc["week"]      = mc.date_aux.dt.week
    mc["day"]      = mc.date_aux.dt.day
    mc["day_name"] = mc.date_aux.dt.day_name(locale='pt_BR.UTF-8')    
    mc["date_ref"] = pd.to_datetime(mc["date_aux"] ,errors = 'coerce',format = '%Y-%m-%d').dt.strftime("%Y-%m-%d")
    mc.drop('date_aux', axis=1, inplace=True)
    return mc


"""
Sobre   : Função responsável por cirar um dataframe 
          que vai conter a dimensão cases.

Entradas: cases_dataframe
            Dataframe que vai originar a dimensão cases

saída   : Dataframe 

"""
def creat_dimension_cases(cases_dataframe):
    prioridade = []
    for i in cases_dataframe["assunto"].str.split(':'):
        if (("Logística" in i[0]) or ("Risco" in i[0]) or
            ("Incidente" in i[0]) or ("Telecom" in i[0])):
            prioridade.append("Alta")
        elif (("Outros" in i[0]) or ("Pedido" in i[0]) or
              ("Produto" in i[0]) or ("Transação" in i[0])):
            prioridade.append("Média")
        else:
            prioridade.append("Baixa")

    cases_dataframe= cases_dataframe.assign(prioridade=prioridade)    
    dim_cases = cases_dataframe[['channelid','missed','pesquisa_de_satisfa_o__c','assunto','prioridade']]
    dim_cases.insert(0, 'cases_key', range(len(cases_dataframe.index)))
    return dim_cases

"""
Sobre   : Função responsável por cirar um dataframe 
          que vai conter a dimensão clientes.

Entradas: cases_dataframe
            Dataframe que vai originar a dimensão cliente

saída   : Dataframe 

"""
def creat_dimension_creds(creds_dataframe):
    dim_creds = creds_dataframe[['accountid','cred_date', 'shipping_address_city', 'shipping_address_state', 'max_machine']]
    dim_creds['accountid'] = dim_creds['accountid'].fillna(0)
    return dim_creds

"""
Sobre   : Função responsável por cirar um dataframe 
          que vai conter a fato cases.

Entradas: cases_dataframe
            Dataframe que vai originar a fato cliente

saída   : Dataframe 

"""
def creat_fact_cases(cases_dataframe):
    fact_cases = cases_dataframe[['date_ref','waitingtime','accountid']]
    fact_cases.insert(0, 'cases_key', range(len(cases_dataframe.index)))
    fact_cases.insert(4, 'count_cases', 1)
    return fact_cases


"""
Sobre   : Função responsável por fazer as leituras
          das bases de dados

Entradas: input_columns:
            Caminho da pasta dos dados.

saída   : Multiplos Dataframe 

"""
def read_data_base(path_data_base):
    cases = pd.read_csv(path_data_base+"cases.csv",index_col=0)
    creds = pd.read_csv(path_data_base+"creds.csv",index_col=0)
    return cases, creds

"""
Sobre   : Função responsável por salvar os dataframes
          em formato csv

Entradas: list_dataframes:
            Lista de dataframe.
          list_names:
            nome como os arquivos vão ser salvos
          output_path:
            Caminho da pasta de saída
saída   : None

"""
def save_dataframes(list_dataframes, list_names, output_path):
    for i in range(0,len(list_dataframes)):
        list_dataframes[i].to_csv(output_path+list_names[i],index=False)
    return