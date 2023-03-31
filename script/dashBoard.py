import streamlit as st
import pandas as pd
#import plotly.express as px
import plotly
import plotly.graph_objects as go

# data
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)
countries = ['Mexico', 'France', 'India']
df = df[df['location'].isin(countries)]

# to date format
df['date'] = pd.to_datetime(df['date'])

# title
st.title('COVID-19 Cases and Deaths')

# Add a filter
metric = st.sidebar.selectbox('Select a metric', ['Cases', 'Deaths'])
data_type = st.sidebar.selectbox('Select a data type', ['Raw', 'Total', '7-day Rolling Average'])

if metric == 'Cases':
    if data_type == 'Raw':
        metric_col = 'new_cases'
        title = 'New Cases'
    elif data_type == 'Total':
        metric_col = 'total_cases'
        title = 'Total Cases'
    elif data_type == '7-day Rolling Average':
        metric_col = 'new_cases_smoothed_per_million'
        title = '7-day Rolling Average of New Cases'
        df[metric_col] = df.groupby('location')[metric_col].rolling(7).mean().reset_index(0, drop=True)
else:
    if data_type == 'Raw':
        metric_col = 'new_deaths'
        title = 'New Deaths'
    elif data_type == 'Total':
        metric_col = 'total_deaths'
        title = 'Total Deaths'
    elif data_type == '7-day Rolling Average':
        metric_col = 'new_deaths_smoothed_per_million'
        title = '7-day Rolling Average of New Deaths'
        df[metric_col] = df.groupby('location')[metric_col].rolling(7).mean().reset_index(0, drop=True)

#country = st.sidebar.selectbox('Select a country', df['location'].unique())
#country = st.sidebar.selectbox('Select a country', ['Mexico', 'France', 'India'])
country = st.sidebar.multiselect("Select countries", df['location'].unique())

date_range = st.sidebar.date_input('Select a date range', [df['date'].min(), df['date'].max()])
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

min_date = df['date'].min().date()
max_date = df['date'].max().date()
start_date, end_date = st.sidebar.select_slider('Select a date range', options=pd.date_range(start=min_date, end=max_date, freq='D'), value=(min_date, max_date))
start_date = start_date.strftime('%Y-%m-%d')
end_date = end_date.strftime('%Y-%m-%d')

# Filter the data based on the selected metric, country, and date range
filtered_data = df[(df['location'].isin(countries)) & (df['date'] >= start_date) & (df['date'] <= end_date)][['date', metric_col]]

# Graph for one country
##fig = go.Figure()
##fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data[metric_col], mode='lines', name=title))
##fig.update_layout(title=title + ' in ' + country)
##st.plotly_chart(fig)

## Graph multiple countries
fig = go.Figure()
for country in countries:
    data = filtered_data[filtered_data['location'] == country]
    fig.add_trace(go.Scatter(x=data['date'], y=data[metric_col], mode='lines', name=title + ' in ' + country))
fig.update_layout(title=title + ' in ' + ', '.join(countries))
st.plotly_chart(fig)