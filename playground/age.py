import requests
from pyaxis import pyaxis
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


filter = {
    "suduroy" : {
        "filter" : "agg:region-en.agg",
        "value": "4600"
    },
    "sandoy" : {
        "filter" : "agg:region-en.agg",
        "value": "4500"
    },
    "tvo" : {
        "filter" : "agg:municipality-en-2017.agg",
        "value": "4602"
    },
    "famjin" : {
        "filter" : "agg:municipality-en-2017.agg",
        "value": "4603"
    },
    "hvalba" : {
        "filter" : "agg:municipality-en-2017.agg",
        "value": "4601"
    },
    "hov" : {
        "filter" : "agg:municipality-en-2017.agg",
        "value": "4604"
    },
    "vag" : {
        "filter" : "agg:municipality-en-2017.agg",
        "value": "4606"
    },
    "sumba" : {
        "filter" : "agg:municipality-en-2017.agg",
        "value": "4607"
    }
}

json_body = {
  "query": [
    {
      "code": "sex",
      "selection": {
        "filter": "item",
        "values": [
          "TOT",
          "M",
          "F"
        ]
      }
    },
    {
      "code": "age",
      "selection": {
        "filter": "item",
        "values": [
          "TOTAL",
          "Y_LT1",
          "Y1",
          "Y2",
          "Y3",
          "Y4",
          "Y5",
          "Y6",
          "Y7",
          "Y8",
          "Y9",
          "Y10",
          "Y11",
          "Y12",
          "Y13",
          "Y14",
          "Y15",
          "Y16",
          "Y17",
          "Y18",
          "Y19",
          "Y20",
          "Y21",
          "Y22",
          "Y23",
          "Y24",
          "Y25",
          "Y26",
          "Y27",
          "Y28",
          "Y29",
          "Y30",
          "Y31",
          "Y32",
          "Y33",
          "Y34",
          "Y35",
          "Y36",
          "Y37",
          "Y38",
          "Y39",
          "Y40",
          "Y41",
          "Y42",
          "Y43",
          "Y44",
          "Y45",
          "Y46",
          "Y47",
          "Y48",
          "Y49",
          "Y50",
          "Y51",
          "Y52",
          "Y53",
          "Y54",
          "Y55",
          "Y56",
          "Y57",
          "Y58",
          "Y59",
          "Y60",
          "Y61",
          "Y62",
          "Y63",
          "Y64",
          "Y65",
          "Y66",
          "Y67",
          "Y68",
          "Y69",
          "Y70",
          "Y71",
          "Y72",
          "Y73",
          "Y74",
          "Y75",
          "Y76",
          "Y77",
          "Y78",
          "Y79",
          "Y80",
          "Y81",
          "Y82",
          "Y83",
          "Y84",
          "Y85",
          "Y86",
          "Y87",
          "Y88",
          "Y89",
          "Y90",
          "Y91",
          "Y92",
          "Y93",
          "Y94",
          "Y95",
          "Y96",
          "Y97",
          "Y98",
          "Y99",
          "Y100",
          "Y101",
          "Y102",
          "Y103",
          "Y104",
          "Y105",
          "Y106",
          "Y107",
          "Y108",
          "Y109",
          "Y110"
        ]
      }
    },
    {
      "code": "village/city",
      "selection": {
        "filter": "agg:municipality-en-2017.agg",
        "values": [
          "4602"
        ]
      }
    }
  ],
  "response": {
    "format": "px"
  }
}

#r = requests.post('https://statbank.hagstova.fo:443/api/v1/en/H2/IB/IB01/fo_abgd_md.px', json = json_body)
#status_code = r.status_code
status_code = 200
print("status code", status_code)
if status_code == 200:
    #with open('age-data.px', 'wb') as outf:
    #    outf.write(r.content)
    px = pyaxis.parse('age-data.px', encoding='utf-8')
    #print(px['DATA'])
    df = px['DATA']
    df['count']=pd.to_numeric(df['DATA'])
    print(df)

    sexes = ["Total (sex)","Males", "Females"]
    #sexes = ["Total (sex)"]
    changes = ["Jan"]
    age_groups = {
        "children": range(1,18),
        "pre school":[1,2,3,4,5],
        "primary school":[6,7,8,9,10,11,12,13,14,15,16],
        "gym":[17,18,19],
        "birth age": range(17,46),
        "working age": range(17,67),
        "old age": range(67,110)
    }


    rdf = pd.DataFrame()
    rdf['year'] = df['year'].loc[(df["sex"] == "Males") & (df['month'] == 'Jan') & (df['age'] == "1 years" )].reset_index()['year']
    for sex in sexes:
        for group in age_groups:
            print(group)
            sdf = pd.DataFrame()
            sdf['year'] = df['year'].loc[(df["sex"] == sex) & (df['month'] == 'Jan') & (df['age'] == "1 years" )].reset_index()['year']
            for year in age_groups[group]:
                sdf[sex + " " + group + " " + str(year) ] = df['count'].loc[(df["sex"] == sex) & (df['month'] == 'Jan') & (df['age'] == str(year) + " years")].reset_index()['count']
            sdf["sum"] = sdf.iloc[:, :len(age_groups[group]) + 1 ].sum(axis=1)
            #print(sdf)
            rdf[sex + " " + group] = sdf["sum"]
    print(rdf.head())

    df_childhood = rdf[["year","Total (sex) pre school", "Total (sex) primary school", "Total (sex) gym"]]
    df_childhood_vs_old = rdf[["year","Total (sex) children", "Total (sex) old age", "Total (sex) working age", "Males working age", "Females working age", "Females birth age"]]
    

    fig = df_childhood_vs_old.plot( x='year', figsize=(12,9), title="Tvøroyrar kommuna demographic development")
    plt.legend(['Under 18', 'Over 67', "18-66", "Males 18-66", "Females 18-66", "Women 18-47"])
    plt.show()
