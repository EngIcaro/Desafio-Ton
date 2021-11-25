#%%
import pandas as pd
import seaborn as sns
#%%
cases = pd.read_csv("../input/cases.csv")
creds = pd.read_csv("../input/creds.csv")
# %%
cases.info()
creds.info()
# %%
print(cases.accountid.nunique())
# %% date_interval
date_interval = pd.to_datetime(cases.date_ref,format="%Y/%m/%d")
print(date_interval.dtype)
#%%
date_interval = date_interval.dt.strftime('%Y-%m-%d')
print(date_interval.min())
print(date_interval.max())
#%% Channelid
print(cases.groupby('channelid').channelid.count())
#%% waitingtime
cases_waitint= cases.copy()
print(cases_waitint.waitingtime.describe())
cases_waitint['series_waiting_time'] = cases_waitint['waitingtime'].rank(method='first')
cases_waitint.sort_values(by=['series_waiting_time'],ascending=False,inplace=True)
highest_waitint = cases_waitint[:144]
#sns.countplot(cases.waitingtime)
# %% missed
# plotando a quantidade de chamados perdidos e quantos de chamados atendidos
print(cases.groupby('missed')['missed'].count())
# %% pesquisa_de_satisfa_o c
print(cases.groupby('pesquisa_de_satisfa_o__c')['pesquisa_de_satisfa_o__c'].count())
print((cases.groupby('pesquisa_de_satisfa_o__c').size()/cases['pesquisa_de_satisfa_o__c'].count())*100)
#%%
print(cases.groupby('assunto')['assunto'].count())
# %% ANalisar a data de credenciamento e seu range
date_interval_cred = pd.to_datetime(creds.cred_date,format="%Y/%m/%d")
print(date_interval_cred.min())
print(date_interval_cred.max())
#%% Analisando a quantidade de clientes por estado
print(creds.groupby('shipping_address_state')['shipping_address_state'].count())
#%%
print(creds.groupby('max_machine')['max_machine'].count())
# %%
