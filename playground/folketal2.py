import requests
from pyaxis import pyaxis
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import matplotlib.style as style
style.use('fivethirtyeight')


def style_fig(fig, title, subtitle, footer):
    import matplotlib.style as style
    style.use('fivethirtyeight')
    fig.tick_params(axis = 'both', which = 'major', labelsize = 18)
    fig.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)
    fig.xaxis.label.set_visible(False)

    

    fig.axes.annotate('...Additional information...',
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=14, ha='center', va='bottom',
            backgroundcolor='grey',
            bbox=dict(boxstyle="round", facecolor="lightblue", edgecolor="white"))
    fig.text(
        x = 145, 
        y = -100, 
        s = '©DATAQUEST                                                     Source: National Center for Education Statistics',
        fontsize = 14, 
        color = '#f0f0f0', 
        backgroundcolor = 'grey',
        #horisontalaligment= "center"
    )
    fig.text(x = 0, y = 62.7, s = "The gender gap is transitory - even for extreme cases",
               fontsize = 26, weight = 'bold', alpha = .75)
    fig.text(x = 0, y = 57,
               s = 'Percentage of Bachelors conferred to women from 1970 to 2011 in the US for\nextreme cases where the percentage was less than 20% in 1970',
              fontsize = 19, alpha = .85)


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

json_body["query"][0]["selection"]["filter"] =  filter["tvo"]["filter"]
json_body["query"][0]["selection"]["values"] = [filter["tvo"]["value"]]

r = requests.post('https://statbank.hagstova.fo:443/api/v1/en/H2/IB/IB01/fo_vital_md.px', json = json_body)
print("status code", r.status_code)
if r.status_code == 200:
    with open('people-data.px', 'wb') as outf:
        outf.write(r.content)
    px = pyaxis.parse('people-data.px', encoding='utf-8')
    #print(px['DATA'])
    df = px['DATA']
    df['date']=pd.to_datetime(df['month']+df['year'].astype(str),format='%b%Y')
    df['count']=pd.to_numeric(df['DATA'])
    
    rdf = pd.DataFrame()
    rdf['date'] = df['date'].loc[(df["sex"] == "Males") & (df['changes'] == "Population primo")].reset_index()['date']
    
    sexes = ["Males", "Females"]
    changes = ["Population primo", "Live births" , "Deaths", "Immigration to The Faroe Islands", "Emigration from The Faroe Islands", "Domestic immigration", "Domestic emigration"]
    
    net_columns = {
        "net births" : ["Live births", "Deaths"],
        "net domestic immigration": ["Domestic immigration", "Domestic emigration"],
        "net foreign": ["Immigration to The Faroe Islands", "Emigration from The Faroe Islands"]
    }

    for sex in sexes:
        for change in changes:
            rdf[sex + " " + change] = df['count'].loc[(df["sex"] == sex) & (df['changes'] == change)].reset_index()['count']

    #print(rdf)
    
    plot_columns = []
    for sex in sexes:
        for column in net_columns:
            rdf[sex + " " + column] = rdf[sex + " " + net_columns[column][0]] - rdf[sex + " " + net_columns[column][1]]
            rdf["sum " + sex + " " + column] = rdf[sex + " " + column].cumsum()
            plot_columns.append("sum " + sex + " " + column)
    
    rdf['sum']=rdf[plot_columns]. sum(axis=1)
    plot_columns.insert(0, 'date')
    plot_columns.append("sum")
    #print(rdf)


    dp = rdf[plot_columns]
    dp.drop(dp.tail(1).index,inplace=True)
    #print(dp.head())
    fig = dp.plot( x='date', figsize=(12,9))
    plt.legend(['Males birth-death', 'Males domestic migration', "Males foreign migration", "Females birth-death", "Females domestic migration", "Females foreign migration", "Total"])
    style_fig(fig, "Title", "sub title", "footer")
    plt.show()
    #print(rdf)
    bdf = pd.DataFrame()
    bdf["date"] =  rdf['date']
    bdf["Males birth"] =  rdf['Males Live births']
    bdf["Females birth"] =  rdf['Females Live births']
    bdf["Births"] = rdf['Males Live births'] + rdf['Females Live births']
    bdf1 = bdf.groupby('date', as_index=False)['Births', "Males birth", "Females birth"].sum()
    bdf1a = bdf1.set_index(bdf1['date'].rename('year').dt.year, append=True).swaplevel(0,1)
    
    bdf2 = bdf1a.groupby(['year']).sum()
    

    
    print (bdf2)

    years = bdf2.index.values[:-2]
    births = bdf2['Births'].values.flatten()[:-2]
    births_males = bdf2['Males birth'].values.flatten()[:-2]
    births_females = bdf2['Females birth'].values.flatten()[:-2]
    print(births)
    deg = 4
    coeff_birth = np.polyfit(years, births, deg) #deg of 1 for straight line
    f1_birth = np.poly1d(coeff_birth)

    coeff_male_birth = np.polyfit(years, births_males, deg) #deg of 1 for straight line
    f1_male_birth = np.poly1d(coeff_male_birth)

    coeff_female_birth = np.polyfit(years, births_females, deg) #deg of 1 for straight line
    f1_female_birth = np.poly1d(coeff_female_birth)

    plt.plot(years, f1_birth(years), 'g' )
    plt.plot(years, f1_male_birth(years), 'b')
    plt.plot(years, f1_female_birth(years), 'r')
    plt.plot(years, births, 'go', ms=2)
    plt.plot(years, births_males, 'bo', ms=2)
    plt.plot(years, births_females, 'ro', ms=2)
    plt.legend(['Total', 'Boys', "Girls"])
    plt.show()
    #fig2 = bdf2.plot(  figsize=(12,9))
    