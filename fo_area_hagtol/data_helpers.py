import os
import requests
from pyaxis import pyaxis


def get_filter_data():
    filter = {
        
        "Føroyar" : {
            "px_id": "Total(region)",
            "filter" : "agg:region-en.agg",
            "value": "9999",
            "municipalities":{}
        },
        "Norðoya" : {
            "px_id": "Norðoya region",
            "filter" : "agg:region-en.agg",
            "value": "4100",
            "municipalities": {
                "Fugloyar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4101"
                },
                "Viðareiðis kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4103"
                },
                "Hvannasunds kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4104"
                },
                "Klaksvíkar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4105"
                },
                "Kunoyar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4106"
                }
            }
        },
        "Eysturoyar øki" : {
            "px_id": "Norðoya region",
            "filter" : "agg:region-en.agg",
            "value": "4200",
            "municipalities": {
                "Fuglafjarðar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4203"
                },
                "Eysturkommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4205"
                },
                "Nes kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4206"
                },
                "Runavíkar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4207"
                },
                "Sjóvar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4208"
                }
                ,
                "Eiðis kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4210"
                },
                "Sunda kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4211"
                }
            }
        },
        "Norðstreymoyar øki" : {
            "px_id": "Norðoya region",
            "filter" : "agg:region-en.agg",
            "value": "4300",
            "municipalities": {
                "Kvívíkar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4306"
                },
                "Vestmanna kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4307"
                }
            }
        },
        "Suðurstreymoyar øki" : {
            "px_id": "Norðoya region",
            "filter" : "agg:region-en.agg",
            "value": "4700",
            "municipalities": {
                "Tórshavnar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4701"
                }
            }
        },
        "Vága øki" : {
            "px_id": "Norðoya region",
            "filter" : "agg:region-en.agg",
            "value": "4400",
            "municipalities": {
                "Vága kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4402"
                },
                "Sørvágs kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4403"
                }
            }
        },
        
        "Sandoy" : {
            "px_id": "Sandoyar region",
            "filter" : "agg:region-en.agg",
            "value": "4500",
            "municipalities":{
               "Skopunar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4502"
                },
                "Sands kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4501"
                },
                "Skálavíkar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4503"
                },
                "Húsavíkar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4504"
                },
                "Skúgvoyar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4505"
                } 
            }
        },
        "Suðuroy" : {
            "px_id": "Suðuroyar region",
            "filter" : "agg:region-en.agg",
            "value": "4600",
            "municipalities": {
                "Hvalbiar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4601"
                },
                "Tvøroyrar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4602"
                },
                "Fámjins kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4603"
                },
                
                "Hovs kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4604"
                },
                "Porkeris kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4605"
                },
                "Vágs kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4606"
                },
                "Sumbiar kommuna" : {
                    "filter" : "agg:municipality-en-2017.agg",
                    "value": "4607"
                }
            }
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
    if municipality == "Øll" or municipality == None:
        return (filter_data[region]["filter"], filter_data[region]["value"], filter_data[region]["px_id"])
    else:
        return (filter_data[region]["municipalities"][municipality]["filter"], filter_data[region]["municipalities"][municipality]["value"], None)
    
def fetch_data(endpoint, json_body, tmp_file_name, expires = 60):
    temp_dir="px_cache"
    temp_file = f"{temp_dir}/{tmp_file_name}.px"
    

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if os.path.isfile(temp_file):
        print("load", temp_file)
        px = pyaxis.parse(temp_file, encoding='utf-8')
        return px['DATA']
    else:
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
            raise Exception(f"error fetch file, status code: {r.status_code} response: {r.content}") 