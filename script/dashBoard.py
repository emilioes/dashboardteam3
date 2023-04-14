# imports
import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go
import os
import numpy as np

################################################################################
# global variable and initialisation
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
if not os.path.isfile("covid-data.csv"):

    df = pd.read_csv(url)
    df.to_csv("covid-data.csv", sep=",", index=False)

else: df = pd.read_csv("covid-data.csv")
df = df[~df['continent'].isnull()]
df = df[~df['location'].isnull()]
df['date'] = pd.to_datetime(df['date'])
selectedCountries= ["France"]
date = [df[df.location.isin(selectedCountries)].date.min(),df[df.location.isin(selectedCountries)].date.max()]
dataType = "Raw"
variables= "new cases smoothed per million"
dataTypeDict = {"Raw":["new cases smoothed per million", "new deaths smoothed per million"], "Cumulative":["total cases per million", "total deaths per million"], "7-day Rolling Average":["new cases smoothed per million", "new deaths smoothed per million"] }

################################################################################
# functions

# function getCountryList
# this function return as a python list the unique country in
# the dataframe (if a location column exist)
# @param,
# @df, the dataframe to search in
# @countryColumn , name of the column that contains the country info, "location" by default
# @return, the list of unique country found or a default country list if the countryColumn  is not found
def getCountryList(df, countryColumn = "location"):
    if countryColumn  in df.columns:
        return df[countryColumn ].unique().tolist()
    else:
        return ["France", "Mexico", "India"] 


# function getData,
# this function return a filtered dataframe, filtered according to the parameter
# @param,
# @df, the dataframe to search in
# @countries, the list of countries to look for
# @variableCol, list of column name to select
# @start_date, the minimal date to filter
# @end_date, the maximum date to filter
#@return, the filtered dataframe
def getData(data, countries, variableCol, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date= pd.to_datetime(end_date)
    data = data[(data.location.isin(countries)) & (data.date >= start_date) & (data.date <= end_date)]
    return data


# function buildGraph,
# this function will retreave the data we want according to the streamlit interractable object
# and then plot the graph accordingly
# this function is used as a call back function for the modification of the streamlit interractable object
def buildGraph(use_peak_detection=False):
    fig = go.Figure()
    data = getData(df, selectedCountries, variables, date[0], date[1])
    for country in selectedCountries:
        filteredData = data[data.location == country]
        col = variables.replace(" ", "_")
        if dataType == "7-day Rolling Average":
            filteredData[col] = filteredData.groupby('location')[col].rolling(7).mean().reset_index(0, drop=True)
        fig.add_trace(go.Scatter(x=filteredData['date'], y=filteredData[col], mode='lines', name=country))

        # Calculate the first derivative of cumulative data
        if dataType == "Cumulative" and use_peak_detection:
            y = filteredData[col]
            x = np.arange(len(y))
            dy = np.gradient(y, x)*20
            fig.add_trace(go.Scatter(x=filteredData['date'], y=dy, mode='lines', name=f"{country} (1st derivative)"))

    title = str.upper(variables[0]) + variables[1:]
    fig.update_layout(title=title + ' in ' + ', '.join(selectedCountries))
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text=title)
    st.plotly_chart(fig)



################################################################################
# building the dashboard interface

#setting the title
st.title('COVID-19 Cases and Deaths')
# setting the interractable elements and their labels
# setting the country selector
st.sidebar.subheader("Select countries:")
selectedCountries = st.sidebar.multiselect("Select countries", getCountryList(df), default= selectedCountries)
# setting the date selector
st.sidebar.subheader("Select date range:")
date = st.sidebar.date_input('Select a date range', [df.date.min(), df.date.max()], min_value= df.date.min(), max_value= df.date.max())
# st.write(date, )

# setting the data type selector
st.sidebar.subheader("Select type of variable to plot:")
dataType = st.sidebar.selectbox('Select a data type', dataTypeDict.keys())
# setting the variable selector,
# the option will change dinamically in function of the data type selected
st.sidebar.subheader("Select variable to plot:")
variables= st.sidebar.selectbox("Variables:", dataTypeDict[dataType])

# setting the peak detection checkbox
st.sidebar.subheader("Peak Detection")
use_peak_detection = st.sidebar.checkbox("Enable peak detection")
buildGraph(use_peak_detection)

#buildGraph()