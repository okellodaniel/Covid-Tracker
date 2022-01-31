# Library imports
import streamlit as st
import pandas as pd
import numpy as np
import requests
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from pandas.io.json import json_normalize
from streamlit.script_runner import RerunException


fig = go.Figure()
st.write("""
        #  Covid 19 Tracking App 🚑
         """)
st.write("""
         This is a web app build by CIT Group 6 Cohort 2, that tracks the covid 19 cases in the world.
         """)

url = "https://api.covid19api.com/countries"
req = requests.get(url)
df0 = json_normalize(req.json())

top_row = pd.DataFrame(
    {'Country': ['Select a Country'], 'Slug': ['Empty'], 'ISO2': ['E']})

# Concatenate with the old frame and reset the Index
df0 = pd.concat([top_row, df0]).reset_index(drop=True)

st.sidebar.header('Create/Filter search')
graph_type = st.sidebar.selectbox(
    'Cases type', ('confirmed', 'deaths', 'recovered'))
st.sidebar.subheader('Search by country')
country1 = st.sidebar.selectbox('Country', df0.Country)
country2 = st.sidebar.selectbox('Compare with another country', df0.Country)

if st.sidebar.button('Refresh Data'):
    raise RerunException(st.ScriptRequestQueue.RerunData(None))

if country1 != 'Select a Country':
    slug = df0.Slug[df0['Country'] == country1].to_string(index=False)[1:]
    url = 'https://api.covid19api.com/dayone/country/'+slug+'/status/'+graph_type
    r = requests.get(url)
    st.write("""
             # Total""" + graph_type + """ cases in """ + country1 + """+are : """+str(r.json()[-1].get("Cases")))
    df = json_normalize(r.json())
    layout = go.Layout(
        title=country1 + '\'s ' + graph_type + ' cases Data',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Number of cases'),
    )

    fig.update_layout(dict1=layout, overwrite=True)
    fig.add_trace(go.Scatter(x=df.Date, y=df.Cases,
                  mode='lines', name=country1))

    if country2 != 'Select a Country':
        slug1 = df0.Slug(df0['Country'] == country2).to_string(index=False)[1:]
        url = 'https://api.covid19api.com/total/dayone/country/'+slug1+'/status/'+graph_type
        r = requests.get(url)
        st.write("""#Total """ + graph_type + """ cases in """ + country2 + """+are : """ +
                 str(r.json()[-1].get("Cases")))
        df = json_normalize(r.json())
        layout = go.Layout(
            title=country2 + ' vs ' + graph_type + ' cases Data',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Number of cases'),
        )
    fig.update_layout(dict1=layout, overwrite=True)
    fig.add_trace(go.Scatter(x=df.Date, y=df.Cases,
                  mode='lines', name=country2))

else:
    url = 'https://api.covid19api.com/world/total'
    r = requests.get(url)
    total = r.json()['TotalConfrimed']
    deaths = r.json()['TotalDeaths']
    recovered = r.json()['TotalRecovered']
    st.write("""
                # WordlWide Data
                """)
    st.write("Total cases: "+str(total)+", Total deaths: " +
             str(deaths)+", Total recovered: "+str(recovered))
    x = ["TotalCases", "TotalDeaths", "TotalRecovered"]
    y = [total, deaths, recovered]

    layout = go.layout(
        title='World Data',
        xaxis=dict(title="Category"),
        yaxis=dict(title="Number of cases")
    )

    fig.update_layout(dict1=layout, overwrite=True)
    fig.add_trace(go.Bar(name='World Data', x=x, y=y))
    st.plotly_chart(fig, use_container_width=True)
