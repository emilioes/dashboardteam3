import plotly.graph_objects as go

# Load the data
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Convert the date column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Set the title of the app
st.title('COVID-19 Cases and Deaths')

# Add a filter for selecting the metric (cases or deaths)
metric = st.sidebar.selectbox('Select a metric', ['Cases', 'Deaths'])

# Add a filter for selecting the type of data to display (new cases/deaths, total cases/deaths, or 7-day rolling average)
data_type = st.sidebar.selectbox('Select a data type', ['New', 'Total', '7-day Rolling Average'])

# Map the selected metric and data type to the appropriate column names
if metric == 'Cases':
    if data_type == 'New':
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
    if data_type == 'New':
        metric_col = 'new_deaths'
        title = 'New Deaths'
    elif data_type == 'Total':
        metric_col = 'total_deaths'
        title = 'Total Deaths'
    elif data_type == '7-day Rolling Average':
        metric_col = 'new_deaths_smoothed_per_million'
        title = '7-day Rolling Average of New Deaths'
        df[metric_col] = df.groupby('location')[metric_col].rolling(7).mean().reset_index(0, drop=True)

# Add a filter for selecting a specific country
#country = st.sidebar.selectbox('Select a country', df['location'].unique())
country = st.sidebar.selectbox('Select a country', ['Mexico', 'France', 'India'])
# Add a date range filter using two date pickers
date_range = st.sidebar.date_input('Select a date range', [df['date'].min(), df['date'].max()])
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Add a date range filter using a double slider
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