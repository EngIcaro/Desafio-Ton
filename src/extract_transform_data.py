#%% Importando my_functions
from my_functions import * 
#%% Main


cases,creds = read_data_base("../input/")

clean_cases= remove_trash(['accountid', 'date_ref'], cases)
clean_creds= remove_trash(['cred_date', 'shipping_address_state'], creds)

clean_creds= remove_duplicates_rows(['cred_date','shipping_address_city' ,'shipping_address_state', 'max_machine', 'accountid'], clean_creds)

master_calendar = creat_master_Calendar(clean_cases['date_ref'])

dim_cases  = creat_dimension_cases(clean_cases)
dim_creds  = creat_dimension_creds(clean_creds)
fact_cases = creat_fact_cases(clean_cases)

#%%
save_dataframes([dim_cases, dim_creds, fact_cases, master_calendar],['dim_cases.csv', 'dim_creds.csv','fact_cases.csv', 'master_calendar.csv'],"../output/")
