import requests
from pyaxis import pyaxis
import pandas as pd
import matplotlib.pyplot as plt

json_body = {
  "query": [
    {
      "code": "village/city",
      "selection": {
        "filter": "agg:municipality-en-2017.agg",
        "values": [
          "4602"
        ]
      }
    },
    {
      "code": "month",
      "selection": {
        "filter": "item",
        "values": [
          "M01",
          "M02",
          "M03",
          "M04",
          "M05",
          "M06",
          "M07",
          "M08",
          "M09",
          "M10",
          "M11",
          "M12"
        ]
      }
    },
    {
      "code": "sex",
      "selection": {
        "filter": "item",
        "values": [
          "M",
          "F"
        ]
      }
    }
  ],
  "response": {
    "format": "px"
  }
}


{
    "date": {
        "mask_column": "changes",
        "mask_value": "Population primo"
    } 
}

r = requests.post('https://statbank.hagstova.fo:443/api/v1/en/H2/IB/IB01/fo_vital_md.px', json = json_body)
print("status code", r.status_code)
if r.status_code == 200:
    with open('data.px', 'wb') as outf:
        outf.write(r.content)
    px = pyaxis.parse('data.px', encoding='utf-8')
    print(px['DATA'])
    mask_primo = (px['DATA']['changes'] == "Population primo")
    mask_birth = (px['DATA']['changes'] == "Live births")
    mask_deaths = (px['DATA']['changes'] == "Deaths")
    mask_immigration = (px['DATA']['changes'] == "Immigration to The Faroe Islands")
    mask_domestic_immigration = (px['DATA']['changes'] == "Domestic immigration")
    mask_emigration = (px['DATA']['changes'] == "Emigration from The Faroe Islands")
    mask_domestic_emigration = (px['DATA']['changes'] == "Domestic emigration")
    
    px['DATA']['date']=pd.to_datetime(px['DATA']['month']+px['DATA']['year'].astype(str),format='%b%Y')
    px['DATA']['count']=pd.to_numeric(px['DATA']['DATA'])
    #f = px['DATA'].reset_index([0])
    #f1 = f.pivot_table(values='changes', index=f.index, columns='DATA', aggfunc='first')
    #print(f1.head())
    #f = px['DATA'].reset_index([0])
    print(px['DATA'].head())
    #print("f")
    #print(f.head())
    #ds = px['DATA'][['date', 'changes', 'count', "changes"]].loc[mask_primo]
    df = pd.DataFrame()

    df['date'] = px['DATA'].loc[mask_primo].reset_index()['date']
    df['primo'] = px['DATA']['count'].loc[mask_primo].reset_index()['count']
    df['births'] = px['DATA']['count'].loc[mask_birth].reset_index()['count']
    df['deaths'] = px['DATA']['count'].loc[mask_deaths].reset_index()['count']
    df['immigration'] = px['DATA']['count'].loc[mask_immigration].reset_index()['count']
    df['emigration'] = px['DATA']['count'].loc[mask_emigration].reset_index()['count']
    df['domestic immigration'] = px['DATA']['count'].loc[mask_domestic_immigration].reset_index()['count']
    df['domestic emigration'] = px['DATA']['count'].loc[mask_domestic_emigration].reset_index()['count']

    df['net_birth'] = df['births'] - df['deaths']
    df['net_immigration'] = df['immigration'] - df['emigration'] 
    df['net_domestic_immigration'] = df['domestic immigration'] - df['domestic emigration'] 

    df['sum_immigration'] = df['net_immigration'].cumsum()
    df['sum_domestic_immigration'] = df['net_domestic_immigration'].cumsum()
    df['sum_birth'] = df['net_birth'].cumsum()

    df['sum'] = df['sum_immigration'] + df['sum_domestic_immigration'] + df['sum_birth']

    print(df)
    
    mask = (df['date'] > '2020-1-1')

    dp = df[['date', 'sum_immigration', 'sum_domestic_immigration', 'sum_birth', 'sum']]

    print(dp.head())
    fig = dp.plot( x='date', figsize=(12,9))
    plt.show()
    #px['DATA'].plot(y='DATA', x='month-year', figsize=(9,6))
    #print(px['METADATA'])
else:
    print(r.text)