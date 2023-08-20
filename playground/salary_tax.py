import requests
from pyaxis import pyaxis
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.style as style
style.use('fivethirtyeight')


def boxplot(df, ax=None, box_width=0.2, whisker_size=20, mean_size=10, median_size = 10 , line_width=1.5, xoffset=0,
                     color=0):
    """Plots a boxplot from existing percentiles.

    Parameters
    ----------
    df: pandas DataFrame
    ax: pandas AxesSubplot
        if to plot on en existing axes
    box_width: float
    whisker_size: float
        size of the bar at the end of each whisker
    mean_size: float
        size of the mean symbol
    color: int or rgb(list)
        If int particular color of property cycler is taken. Example of rgb: [1,0,0] (red)

    Returns
    -------
    f, a, boxes, vlines, whisker_tips, mean, median
    """

    if type(color) == int:
        color = plt.rcParams['axes.prop_cycle'].by_key()['color'][color]

    if ax:
        a = ax
        f = a.get_figure()
    else:
        f, a = plt.subplots()

    boxes = []
    vlines = []
    xn = []
    for row in df.iterrows():
        #x = row[1]["label"]
        x= .5
        xn.append(row[1]["label"][:-6])

        # box
        y = row[1][25]
        height = row[1][75] - row[1][25]
        box = plt.Rectangle((x - box_width / 2, y), box_width, height)
        a.add_patch(box)
        boxes.append(box)

        # whiskers
        y = (row[1][90] + row[1][10]) / 2
        vl = a.vlines(x, row[1][10], row[1][90])
        vlines.append(vl)

    for b in boxes:
        b.set_linewidth(line_width)
        b.set_facecolor([1, 1, 1, 1])
        b.set_edgecolor(color)
        b.set_zorder(2)

    for vl in vlines:
        vl.set_color(color)
        vl.set_linewidth(line_width)
        vl.set_zorder(1)

    whisker_tips = []
    if whisker_size:
        g, = a.plot(xn, df[10], ls='')
        whisker_tips.append(g)

        g, = a.plot(xn, df[90], ls='')
        whisker_tips.append(g)

    for wt in whisker_tips:
        wt.set_markeredgewidth(line_width)
        wt.set_color(color)
        wt.set_markersize(whisker_size)
        wt.set_marker('_')

    mean = None
    if mean_size:
        g, = a.plot(xn, df[50], ls='')
        g.set_marker('o')
        g.set_markersize(mean_size)
        g.set_zorder(20)
        g.set_markerfacecolor('None')
        g.set_markeredgewidth(line_width)
        g.set_markeredgecolor(color)
        mean = g

    median = None
    if median_size:
        g, = a.plot(xn, df['median'], ls='')
        g.set_marker('_')
        g.set_markersize(median_size)
        g.set_zorder(20)
        g.set_markeredgewidth(line_width)
        g.set_markeredgecolor(color)
        median = g

    a.set_xticklabels(xn, rotation = 45)
    #a.set_ylim(np.nanmin(df), np.nanmax(df))
    return f, a, boxes, vlines, whisker_tips, mean, median


def box_plot_2(percentiles, *args, **kwargs):
    """
    Generates a customized boxplot based on the given percentile values
    """
    redraw = True

    labels = []
      
    f, a = plt.subplots()
    f.subplots_adjust(bottom=0.2)
    box_plot = a.boxplot([[-9, -4, 2, 4, 9],]*len(percentiles), *args, **kwargs) 
    # Creates len(percentiles) no of box plots
    
    min_y, max_y = float('inf'), -float('inf')
    
    for box_no, (label,
                 q1_start, 
                 q2_start,
                 q3_start,
                 q4_start,
                 q4_end,
                 fliers_xy) in enumerate(percentiles):
        
    
        labels.append(label)
        # Lower cap
        box_plot['caps'][2*box_no].set_ydata([q1_start, q1_start])
        # xdata is determined by the width of the box plot

        # Lower whiskers
        box_plot['whiskers'][2*box_no].set_ydata([q1_start, q2_start])

        # Higher cap
        box_plot['caps'][2*box_no + 1].set_ydata([q4_end, q4_end])

        # Higher whiskers
        box_plot['whiskers'][2*box_no + 1].set_ydata([q4_start, q4_end])

        # Box
        box_plot['boxes'][box_no].set_ydata([q2_start, 
                                             q2_start, 
                                             q4_start,
                                             q4_start,
                                             q2_start])
        
        # Median
        box_plot['medians'][box_no].set_ydata([q3_start, q3_start])

        # Outliers
        if fliers_xy is not None and len(fliers_xy[0]) != 0:
            # If outliers exist
            box_plot['fliers'][box_no].set(xdata = fliers_xy[0],
                                           ydata = fliers_xy[1])
            
            min_y = min(q1_start, min_y, fliers_xy[1].min())
            max_y = max(q4_end, max_y, fliers_xy[1].max())
            
        else:
            min_y = min(q1_start, min_y)
            max_y = max(q4_end, max_y)
                    
        # The y axis is rescaled to fit the new box plot completely with 10% 
        # of the maximum value at both ends
        a.set_ylim([min_y*1.1, max_y*1.1])
    a.set_xticklabels(labels, rotation = 45)
    # If redraw is set to true, the canvas is updated.
    #if redraw:
    #    ax.figure.canvas.draw()
        
    return box_plot



api = "https://statbank.hagstova.fo:443/api/v1/fo/H2/IP/IP01/innt_nbs.px"

json_body = {
  "query": [
    {
      "code": "unit",
      "selection": {
        "filter": "item",
        "values": [
          "DKK"
        ]
      }
    },
    {
      "code": "sex",
      "selection": {
        "filter": "item",
        "values": [
          "TOT",
#          "M",
#          "F"
        ]
      }
    },
    {
      "code": "region",
      "selection": {
        "filter": "item",
        "values": [
          "9999",
          "4100",
          "4200",
          "4300",
          "4700",
          "4400",
          "4500",
          "4600"
        ]
      }
    },
    {
      "code": "age",
      "selection": {
        "filter": "item",
        "values": [
          "Y_GE15"
          
        ]
      }
    },
    {
      "code": "year",
      "selection": {
        "filter": "item",
        "values": [
          #"2021",
          "2020",
          "2019",
          "2018",
          "2017",
          "2016",
          "2015",
          "2014",
          "2013",
          "2012",
          "2011",
          "2010",
          "2009"

#          "2015",
#          "2010"
        ]
      }
    },
    {
      "code": "percentile intervals",
      "selection": {
        "filter": "item",
        "values": [
          "P1_AVG",
          "P10_AVG",
          "P25_AVG",
          "P50_AVG",
          "P75_AVG",
          "P90_AVG",
#          "P95_AVG",
#          "P99_AVG",
          "P100_AVG"
        ]
      }
    }
  ],
  "response": {
    "format": "px"
  }
}

r = requests.post(api, json = json_body)
status_code = r.status_code
#status_code = 200
print("status code", status_code)
if status_code == 200:
    with open('salary-data.px', 'wb') as outf:
        outf.write(r.content)
    px = pyaxis.parse('salary-data.px', encoding='utf-8')
    #print(px['DATA'])
    df = px['DATA']
    df['count']=pd.to_numeric(df['DATA'])
    df.drop('age', axis=1, inplace=True)
    df.drop('unit', axis=1, inplace=True)
    print(df)

    #gk = df.groupby("region")
    #print(gk)
    #print( gk.get_group('Suðuroyar region'))
    #rdf = gk.get_group('Suðuroyar region')

    sdf = pd.DataFrame()

    measure = "Gross income"
    year = "2020"

    fdf = df
    sdf['year'] = fdf['year'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "1" )].reset_index()['year']
    sdf['region'] = fdf['region'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "1" )].reset_index()['region']
    #sdf['1'] =  fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "1" )].reset_index()['count']
    sdf['10'] = fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "10" )].reset_index()['count']
    sdf['25'] = fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "25" )].reset_index()['count']
    sdf['50'] = fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "50" )].reset_index()['count']
    sdf['75'] = fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "75" )].reset_index()['count']
    sdf['90'] = fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "90" )].reset_index()['count']
    #sdf['100'] = fdf['count'].loc[(fdf["measure"] == measure ) & (fdf["sex"] == "Total (sex)") &(fdf["percentile intervals"] == "100" )].reset_index()['count']
    print(sdf)

    
    
    gk = sdf.groupby("year")
    #years = list(sdf["year"].drop_duplicates())
    g = gk.get_group('2020')
    bxf = pd.DataFrame()
    bxf["label"] = g["region"]
    bxf["median"] =  g['50']
    bxf["mean"] =  g['50']
    bxf[10] = g['10']
    bxf[25] = g['25']
    bxf[50] =  g['50']
    bxf[75] = g['75']
    bxf[90] = g['90']

    box_data = []
    for row in bxf.iterrows():
        #x = row[1]["label"]
        box_data.append([
            row[1]["label"][:-6],
            row[1][10],
            row[1][25],
            row[1][50],
            row[1][75],
            row[1][90],
            None
        ])
        
    box_plot_2(box_data, )
    #out = boxplot(bxf)

    print(gk.get_group('2020'))

    gkr = sdf.groupby("region")

    gkrx = gkr.get_group('Suðuroyar region')
    #print(gkrx)

    #print(gkr)

    #gkr.get_group('2020').plot(x="year", figsize=(12,9), kind="box")
    #gkrx.boxplot(x="year", figsize=(12,9))
    plt.show()


