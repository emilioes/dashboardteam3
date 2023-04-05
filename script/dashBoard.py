# imports
import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go


################################################################################
# global variable and initialisation
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)
df = df[~df['continent'].isnull()]
df = df[~df['location'].isnull()]
df['date'] = pd.to_datetime(df['date'])
selectedCountries= ["France"]
date = [df[df.location.isin(selectedCountries)].date.min(),df[df.location.isin(selectedCountries)].date.max()]
dataType = "Raw"
variables= ["new_cases"]
dataTypeDict = {"Raw":["new_cases", "new_deaths"], "Total":["total_cases", "total_deaths"], "7-day Rolling Average":["new_cases_smoothed_per_million", "new_deaths_smoothed_per_million"] }

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
@return, the filtered dataframe
def getData(data, countries, variableCol, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date= pd.to_datetime(end_date)
    data = data[(data.location.isin(countries)) & (data.date >= start_date) & (data.date <= end_date)]
    return data
# function buildGraph,
# this function will retreave the data we want according to the streamlit interractable object
# and then plot the graph accordingly
# this function is used as a call back function for the modification of the streamlit interractable object
def buildGraph():
    fig = go.Figure()
    data = getData(df, selectedCountries, variables, date[0], date[1])
    for country in selectedCountries:
        filteredData = data[data.location == country]
        for var in variables:
            if dataType == "7-day Rolling Average":
                filteredData[var] = filteredData.groupby('location')[var].rolling(7).mean().reset_index(0, drop=True)


            fig.add_trace(go.Scatter(x=filteredData['date'], y=filteredData[var], mode='lines', name=country))
    title = "".join([s.replace("_", " ") for s in variables])
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
selectedCountries = st.sidebar.multiselect("Select countries", getCountryList(df), default= selectedCountries, on_change= buildGraph())
# setting the date selector
st.sidebar.subheader("Select date range:")
date = st.sidebar.date_input('Select a date range', [df.date.min(), df.date.max()], min_value= df.date.min(), max_value= df.date.max(), on_change= buildGraph())
st.write(date, )

# setting the data type selector
st.sidebar.subheader("Select type of variable to plot:")
dataType = st.sidebar.selectbox('Select a data type', dataTypeDict.keys())
# setting the variable selector,
# the option will change dinamically in function of the data type selected
st.sidebar.subheader("Select variable to plot:")
variables= st.sidebar.multiselect("Variables:", dataTypeDict[dataType], default=dataTypeDict[dataType ][0], on_change= buildGraph())
