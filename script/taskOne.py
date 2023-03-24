import streamlit as st
import pandas as pd
import plotly.express as px



# Crypto monthly data
d = {'Month':[1,2,3,4,5,6,7,8,9,10,11],
     'Bitcoin':[47733,38777,44404,46296,38471,29788,19247,23273,20146,19315,20481],
     'Ethereum':[3767,2796,2973,3448,2824,1816,1057,1630,1587,1311,1579]}

cryptodf = pd.DataFrame(data = d)

# The Incredible Widget Company
d = {'Quarter':[1,2,3,4],
     'Widgets':[100,110,112,120],
     'Wodgets':[50,100,120, 125],
     'Wudgets':[200,150,100,90]}
     
salesdf = pd.DataFrame(d)

btcCurrent = 16080
btcYrBeg = 47733
btcdelta = btcCurrent - btcYrBeg

st.metric("Bitcoin", btcCurrent, delta=btcdelta, delta_color="normal", 
          help="Change in Bitcoin dollar value since the year beginning")

st.table(cryptodf)

## covid
import altair as alt

df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

df = df[df["people_fully_vaccinated"].notnull()]

# Convert the date column to a datetime object
df["date"] = pd.to_datetime(df["date"])

st.title("COVID-19 Vaccination Data")
st.write("This app displays the number of people fully vaccinated against COVID-19 over time.")
    
    # Create a line chart using Altair
chart = alt.Chart(df).mark_line().encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("people_fully_vaccinated:Q", title="People Fully Vaccinated")
    ).properties(
        width=800,
        height=500
    )

    # Display the chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)


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

# Display the chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)

df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
###
countries = ['United States', 'India', 'Mexico', 'France']
country_cases = df.loc[df['location'].isin(countries)]
country_cases = country_cases.groupby(['location', 'date'])['new_cases_smoothed_per_million'].sum().reset_index()

fig = px.line(country_cases, x='date', y='new_cases_smoothed_per_million', color='location', title='Daily New COVID-19 Cases')
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

