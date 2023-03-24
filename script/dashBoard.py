import streamlit as st
import pandas as pd
import plotly

##
import pandas as pd
import streamlit as st

df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', 
                 usecols = ['continent', 'location', 'new_cases_per_million', 'date'])

# Select and filter by Continent
df = df[df['continent'].notna()]
continent_filter = st.selectbox("Select the Continent", pd.unique(df["continent"]))
df = df[df["continent"] == continent_filter]
df = df.drop(columns='continent')

# Create Matrix with location x date
df = df.pivot(index='date', columns='location')
df.columns = [item[1] for item in list(df.columns.to_flat_index())]

# Create dashboard
st.title("New Covid-19 cases per million per country")
st.line_chart(df)


df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
###
countries = ['United States', 'India', 'Mexico', 'France']
country_cases = df.loc[df['location'].isin(countries)]
country_cases = country_cases.groupby(['location', 'date'])['new_cases_smoothed_per_million'].sum().reset_index()

fig = plotly.line(country_cases, x='date', y='new_cases_smoothed_per_million', color='location', title='Daily New COVID-19 Cases')
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='new_cases_smoothed_per_million',
    legend_title='Country',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    )
)

st.plotly_chart(fig)


