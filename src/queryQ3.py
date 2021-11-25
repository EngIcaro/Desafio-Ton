# %%
# Realizando os join
result_dataframe = fact_cases.merge(dim_cases, on='cases_key', how='left')
result_dataframe = result_dataframe.merge(master_calendar, on='date_ref', how='left')    
# Realizando as query
result_dataframe = result_dataframe.query("month == 10 or month == 9 or month == 8")
# Somando o valor por Mês e prioridade
result_dataframe.groupby(['prioridade','month_name','week'])['count_cases'].sum()