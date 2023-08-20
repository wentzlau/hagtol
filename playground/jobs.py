import requests
from pyaxis import pyaxis
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

json_body = {
  "query": [
    {
      "code": "month",
      "selection": {
        "filter": "item",
        "values": [
          "2019M01",
          "2020M01",
          "2021M01",
          "2022M01",
          "2023M01"
        ]
      }
    },
    {
      "code": "industry",
      "selection": {
        "filter": "agg:industry-group-fo.agg",
        "values": [
          "VGTOT",
          "VGB1",
          "RE",
          "LB",
          "FS",
          "AK",
          "FV",
          "OS",
          "VGB2",
          "BY",
          "SK",
          "OV",
          "ID",
          "VGB3",
          "HU",
          "GI",
          "SJ",
          "FL",
          "FM",
          "PO",
          "FT",
          "VT",
          "HT",
          "VGB4",
          "LF",
          "KR",
          "UV",
          "HA"
        ]
      }
    },
    {
      "code": "region",
      "selection": {
        "filter": "item",
        "values": [
          "4600"
        ]
      }
    },
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
          "Y_16-74",
          "Y16-19",
          "Y20-24",
          "Y25-39",
          "Y40-54",
          "Y55-66",
          "Y67-74"
        ]
      }
    }
  ],
  "response": {
    "format": "px"
  }
}

sexes = ["Bæði kyn","Mannfólk","Konufólk"]
age_groups=["Tils. (16-74 ár)","16-19 ár","20-24 ár","25-39 ár","40-54 ár","55-66 ár","67-74 ár"]
main_types = {
    "FISKIVINNA O.O. TILFEINGISVINNA": ["- Ráevnisvinna","- Landbúnaður","- Fiskiskapur","- Ali-og kryvjivirki","- Fiskavøruídnaður","- Ótilskilað v.m."],
    "BYGGIVINNA O.O. TILVIRKING": ["- Bygging","- Skipasmiðjur, smiðjur", "- Orku- og vatnveiting","- Annar ídnaður"],
    "PRIVATAR TÆNASTUVINNUR": ["- Handil og umvæling","- Gistihús og matstovuvirki","- Sjóflutningur","- Flutningur annars","- Felagsskapir, mentan o.a.","- Postur og fjarskifti","- Fígging og trygging","- Vinnuligar tænastur","- Húshaldstænastur"],
    "ALMENN O.O. TÆNASTA": [ "- Landsfyrisiting","- Kommunur og ríkisstovnar","- Undirvísing","-  Heilsu- og almannaverk"]
}

sub_types = ["Tils. (vinnnugrein)","FISKIVINNA O.O. TILFEINGISVINNA","- Ráevnisvinna","- Landbúnaður","- Fiskiskapur","- Ali-og kryvjivirki","- Fiskavøruídnaður","- Ótilskilað v.m.","BYGGIVINNA O.O. TILVIRKING","- Bygging","- Skipasmiðjur, smiðjur",
"- Orku- og vatnveiting","- Annar ídnaður","PRIVATAR TÆNASTUVINNUR","- Handil og umvæling","- Gistihús og matstovuvirki","- Sjóflutningur","- Flutningur annars","- Felagsskapir, mentan o.a.","- Postur og fjarskifti","- Fígging og trygging",
"- Vinnuligar tænastur","- Húshaldstænastur","ALMENN O.O. TÆNASTA","- Landsfyrisiting","- Kommunur og ríkisstovnar","- Undirvísing","-  Heilsu- og almannaverk"]


r = requests.post("https://statbank.hagstova.fo:443/api/v1/fo/H2/AM/AM03/lont_vkaom_t.px", json = json_body)
status_code = r.status_code
#status_code = 200
print("status code", status_code)
if status_code == 200:
    with open('job-data.px', 'wb') as outf:
        outf.write(r.content)
    px = pyaxis.parse('job-data.px', encoding='utf-8')
    #print(px['DATA'])
    df = px['DATA']
    df['count']=pd.to_numeric(df['DATA'])
    print(df)