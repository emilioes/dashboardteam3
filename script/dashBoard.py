import streamlit as st
import pandas as pd
import plotly

df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
###
df = df[(df["location"] == "Mexico") & (df["people_fully_vaccinated"].notnull())]

# Convert the date column to a datetime object
df["date"] = pd.to_datetime(df["date"])

st.title("COVID-19 Vaccination Data for Mexico")
st.write("This app displays the number of people fully vaccinated against COVID-19 in Mexico over time.")
    
# Create a line chart using Altair
chart = alt.Chart(df).mark_line().encode(
   x=alt.X("date:T", title="Date"),
   y=alt.Y("people_fully_vaccinated:Q", title="People Fully Vaccinated")
).properties(
     width=800,
     height=500
)


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


