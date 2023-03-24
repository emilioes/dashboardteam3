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