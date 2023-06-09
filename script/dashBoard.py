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
variables= "Cases"
# dataTypeDict = {"Raw":{"cases":"new_cases_smoothed_per_million", "deathes":"new_deaths_smoothed_per_million"}, "Cumulative":["total cases per million", "total deaths per million"], "7-day Rolling Average":["new cases smoothed per million", "new deaths smoothed per million"] }
dataTypeDict={"Raw":{"Cases":"new_cases_smoothed_per_million", "Deaths":"new_deaths_smoothed_per_million"}, "Cumulative":{"Cases":"total_cases_per_million", "Deaths":"total_deaths_per_million"},"7-day Rolling Average":{"Cases":"new_cases_smoothed_per_million","Deaths":"new_deaths_smoothed_per_million"}}


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
def getData(data, countries, variableCol, startDate, endDate):
    startDate = pd.to_datetime(startDate)
    endDate= pd.to_datetime(endDate)
    data = data[(data.location.isin(countries)) & (data.date >= startDate) & (data.date <= endDate)]
    return data


# function buildGraph,
# this function will retreave the data we want according to the streamlit interractable object
# and then plot the graph accordingly
# this function is used as a call back function for the modification of the streamlit interractable object
def buildGraph(use_peak_detection=False):
    fig = go.Figure()
    data = getData(df, selectedCountries, variables, date[0], date[1])
    for i, country in enumerate(selectedCountries):
        filteredData = data[data.location == country]
        col = dataTypeDict[dataType][variables]
        if dataType == "7-day Rolling Average":
            filteredData[col] = filteredData.groupby('location')[col].rolling(7).mean().reset_index(0, drop=True)
        fig.add_trace(go.Scatter(x=filteredData['date'], y=filteredData[col], mode='lines', name=country))

        # Calculate the first derivative of cumulative data
        if dataType == "Cumulative" and use_peak_detection and i ==0:
            y = filteredData[col]
            x = np.arange(len(y))
            # we compute the numerical derivative to find the peaks, we multiply by 20 to make them more visible on the graph
            peaks = np.gradient(y, x)*20
            fig.add_trace(go.Scatter(x=filteredData['date'], y=peaks, mode='lines', name=f"{country} (1st derivative)"))

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
variables= st.sidebar.selectbox("Variables:", dataTypeDict[dataType].keys())

# setting the peak detection checkbox
if dataType == "Cumulative" :
    st.sidebar.subheader("Peak Detection")
    use_peak_detection = st.sidebar.checkbox("Enable peak detection")
else:
    use_peak_detection = False

# calling the function to plot our variables
buildGraph(use_peak_detection)