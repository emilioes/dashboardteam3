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
country = st.sidebar.selectbox('Select a country', ['Mexico', 'France', 'India'])

date_range = st.sidebar.date_input('Select a date range', [df['date'].min(), df['date'].max()])
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

min_date = df['date'].min().date()
max_date = df['date'].max().date()
start_date, end_date = st.sidebar.select_slider('Select a date range', options=pd.date_range(start=min_date, end=max_date, freq='D'), value=(min_date, max_date))

# Filter the data based on the selected metric, country, and date range
filtered_data = df[(df['location'] == country) & (df['date'] >= start_date) & (df['date'] <= end_date)][['date', metric_col]]

# Create the graph using Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data[metric_col], mode='lines', name=title))
fig.update_layout(title=title + ' in ' + country)
st.plotly_chart(fig)

# Crypto monthly data
##d = {'Month':[1,2,3,4,5,6,7,8,9,10,11],
##     'Bitcoin':[47733,38777,44404,46296,38471,29788,19247,23273,20146,19315,20481],
##     'Ethereum':[3767,2796,2973,3448,2824,1816,1057,1630,1587,1311,1579]}

##cryptodf = pd.DataFrame(data = d)
##
### The Incredible Widget Company
##d = {'Quarter':[1,2,3,4],
##     'Widgets':[100,110,112,120],
##     'Wodgets':[50,100,120, 125],
##     'Wudgets':[200,150,100,90]}
##     
##salesdf = pd.DataFrame(d)
##
##btcCurrent = 16080
##btcYrBeg = 47733
##btcdelta = btcCurrent - btcYrBeg
##
##st.metric("Bitcoin", btcCurrent, delta=btcdelta, delta_color="normal", 
##          help="Change in Bitcoin dollar value since the year beginning")
##
##st.table(cryptodf)
##
#### covid
##import altair as alt
##
##df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
##
##df = df[df["people_fully_vaccinated"].notnull()]
##
### Convert the date column to a datetime object
##df["date"] = pd.to_datetime(df["date"])
##
##st.title("COVID-19 Vaccination Data")
##st.write("This app displays the number of people fully vaccinated against COVID-19 over time.")
##    
##    # Create a line chart using Altair
##chart = alt.Chart(df).mark_line().encode(
##        x=alt.X("date:T", title="Date"),
##        y=alt.Y("people_fully_vaccinated:Q", title="People Fully Vaccinated")
##    ).properties(
##        width=800,
##        height=500
##    )
##
##    # Display the chart in the Streamlit app
##st.altair_chart(chart, use_container_width=True)
##
##
##df = df[(df["location"] == "Mexico") & (df["people_fully_vaccinated"].notnull())]
##
### Convert the date column to a datetime object
##df["date"] = pd.to_datetime(df["date"])
##
##st.title("COVID-19 Vaccination Data for Mexico")
##st.write("This app displays the number of people fully vaccinated against COVID-19 in Mexico over time.")
##    
### Create a line chart using Altair
##chart = alt.Chart(df).mark_line().encode(
##   x=alt.X("date:T", title="Date"),
##   y=alt.Y("people_fully_vaccinated:Q", title="People Fully Vaccinated")
##).properties(
##     width=800,
##     height=500
##)
##
### Display the chart in the Streamlit app
##st.altair_chart(chart, use_container_width=True)

##df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
#####
##countries = ['United States', 'India', 'Mexico', 'France']
##country_cases = df.loc[df['location'].isin(countries)]
##country_cases = country_cases.groupby(['location', 'date'])['new_cases_smoothed_per_million'].sum().reset_index()
##
##fig = plotly.line(country_cases, x='date', y='new_cases_smoothed_per_million', color='location', title='Daily New COVID-19 Cases')
##fig.update_layout(
##    xaxis_title='Date',
##    yaxis_title='new_cases_smoothed_per_million',
##    legend_title='Country',
##    legend=dict(
##        yanchor="top",
##        y=0.99,
##        xanchor="right",
##        x=0.99
##    )
##)
##
##st.plotly_chart(fig)
