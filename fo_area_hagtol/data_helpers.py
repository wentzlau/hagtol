import requests
from pyaxis import pyaxis

def get_filter_data():
    filter = {
        "suduroy" : {
            "filter" : "agg:region-en.agg",
            "value": "4600",
            "municipalities": {
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
            },
        },
        "sandoy" : {
            "filter" : "agg:region-en.agg",
            "value": "4500",
            "municipalities":{}
        }            
        
    }

    return filter

def get_regions():
    filter_data = get_filter_data()
    return list(filter_data.keys())

def get_municipalities(region):
    filter_data = get_filter_data()
    return ["Øll"] + list(filter_data[region]["municipalities"].keys())

def get_filter(region, municipality):
    filter_data = get_filter_data()
    if municipality == "Øll":
        return (filter_data[region]["filter"], filter_data[region]["value"])
    else:
        return (filter_data[region]["municipalities"][municipality]["filter"], filter_data[region]["municipalities"][municipality]["value"])
    
def fetch_data(endpoint, json_body, tmp_file_name):
    temp_file = tmp_file_name + ".px"
    base_url = "https://statbank.hagstova.fo:443/api/"
    r = requests.post( base_url + endpoint, json = json_body)
    #print("status code", r.status_code)
    if r.status_code == 200:
        with open(temp_file, 'wb') as outf:
            outf.write(r.content)
        px = pyaxis.parse(temp_file, encoding='utf-8')
    #print(px['DATA'])
        return px['DATA']
    else:
        raise Exception(f"error fetch file, status code: {r.status_code}") 