import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


import plotly.plotly as py
import plotly.graph_objs as go
from pandas.tools.plotting import scatter_matrix

from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.charts.utils import df_from_json
from bokeh.sampledata import us_states
from bokeh.models import HoverTool
from collections import OrderedDict

class Data_visual(object):
    """docstring for Data_visual."""
    def __init__(self, df):
        self.df = df

    def get_max(self):
        '''
        states have the highest rate of each of the seven crimes
        '''
        max_c=self.df[self.df.columns[1:]].idxmax()
        return zip(max_c.index, self.df.ix[max_c].State)

    def get_min(self):
        min_c=self.df[self.df.columns[1:]].idxmin()
        return zip(min_c.index, self.df.ix[min_c].State)

    def plot_correlation(self):
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.df.corr())
        plt.show()

    def plot_hist(self):
        for crime in self.df.columns[1:]:
            f = plt.figure()
            hist = self.df[crime].hist()
            hist.set_title(crime)
        plt.show()

def plot_kde(df):
    for crime in df.columns[1:]:
        f = plt.figure()
        hist = df[crime].plot(kind='kde')
        hist.set_title(crime)
    plt.show()

def plot_box(df):
    plt.figure(figsize=(14,10))
    sns.boxplot(df)
    plt.show()

def plot_violin(df):
    plt.figure(figsize=(10,8))
    sns.violinplot(df, scale='count', inner='quartile')
    plt.show()

def new_df_index_state(df):
    df2=df.copy()
    df2.set_index(df2.State, inplace=True)
    df2=df2.drop('State',axis =1)
    return df2

def sum_crime(df):
    return sum(df[1:])

def sorted_df(df):
    df['total'] = df.apply(sum_crime, axis=1)
    sorted_df = df.sort_values('total', ascending=False)
    return sorted_df


def plot_stacked_bar_chart(df):
    bar = Bar(df,
              values=blend('Murder', 'Rape', 'Robbery', 'Aggravated Assault', 'Burglary',
                           'Larceny Theft', 'Motor Vehicle Theft', name='Crime', labels_name='crime'),
              label=cat(columns='State', sort=False),
              stack=cat(columns='crime', sort=False),

              legend='top_right',
              title="Crime per state",
              width=1000, height=500,
              tooltips=[('crime', '@crime'), ('state', '@State')]
             )
    #output_file("stacked_bar.html", title="stacked_bar.py example")
    show(bar)

def plot_map(df2):
    from bokeh.sampledata import us_states
    from bokeh.models.sources import ColumnDataSource
    from bokeh.plotting import *
    us_states = us_states.data.copy()
    del us_states["HI"]
    del us_states["AK"]
    states=[a['name'] for a in us_states.values()]
    rates = [df2.ix[state_name]['Larceny Theft'] for state_name in states]
    cm = plt.get_cmap('YlOrRd')
    c_map = plt.cm.ScalarMappable(cmap=cm)
    c_map.set_clim(df2['Larceny Theft'].min(), df2['Larceny Theft'].max())
    state_colors0=[c_map.to_rgba(rate) for rate in rates]
    state_colors = [ (c[0] * 255, c[1] * 255, c[2] * 255) for c in state_colors0 ]
    state_hex = [  ('#%02x%02x%02x' % c) for c in state_colors]

    state_xs = [us_states[code]["lons"] for code in us_states]
    state_ys = [us_states[code]["lats"] for code in us_states]

    TOOLS="pan,wheel_zoom,box_zoom,reset,hover,save"

    source = ColumnDataSource(
        data=dict(
            rate=rates,
            state=states
        )
    )

    p = figure(title="State Crime Rates", toolbar_location="left",
        plot_width=1100, plot_height=700, tools=TOOLS)

    p.patches(state_xs, state_ys, fill_color=state_hex,
        line_color="#884444", line_width=2, source=source)


    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("State", "@state"),
        ('rate', '@rate'),
        ("(x,y)", "($x, $y)"),
    ])

    show(p)

if __name__ == '__main__':
    df = pd.read_csv('crime.csv')
    #print get_max(df)
    #plot_correlation(df)
    #plot_violin(df)
    # sorted_df = sorted_df(df)
    # plot_stacked_bar_chart(sorted_df)
    df2=new_df_index_state(df)
    plot_map(df2)
    # visual = Data_visual(df)
    # print visual.get_min()
