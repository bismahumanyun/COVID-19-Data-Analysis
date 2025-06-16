import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset from Our World in Data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sample a country for time-series plotting (e.g., Canada)
country = 'Canada'
country_df = df[df['location'] == country]

# Create a time-series line chart: cases, deaths, vaccinations
plt.figure(figsize=(14, 6))
plt.plot(country_df['date'], country_df['new_cases'],
         label='New Cases', alpha=0.6)
plt.plot(country_df['date'], country_df['new_deaths'],
         label='New Deaths', alpha=0.6)
plt.plot(country_df['date'], country_df['new_vaccinations'],
         label='New Vaccinations', alpha=0.6)
plt.title(f'COVID-19 Daily Trends in {country}')
plt.xlabel('Date')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.savefig('D:/Git/COVID-19-Data-Analysis/data/covid_timeseries_canada.png')

# Correlation Heatmap (latest available date per country)
latest_df = df.sort_values('date').groupby('location').tail(1)
features = latest_df[['total_deaths_per_million',
                      'gdp_per_capita', 'population_density', 'median_age']].dropna()
correlation_matrix = features.corr()

# Create heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Between COVID-19 Severity and Country Features')
plt.tight_layout()
plt.savefig(
    'D:/Git/COVID-19-Data-Analysis/data/covid_feature_correlation_heatmap.png')

# Vaccination Speed Bar Chart
vacc_df = df[['location', 'date', 'people_vaccinated_per_hundred']].dropna()
vacc_df['date'] = pd.to_datetime(vacc_df['date'])

# Calculate days to 50% vaccinated per country


def days_to_50pct(group):
    group = group.sort_values('date')
    start_date = group['date'].iloc[0]
    reached_50 = group[group['people_vaccinated_per_hundred'] >= 50]
    if not reached_50.empty:
        date_50 = reached_50['date'].iloc[0]
        return (date_50 - start_date).days
    else:
        return pd.NA


vacc_speed = vacc_df.groupby('location').apply(
    days_to_50pct).dropna().sort_values().head(10)

# Bar chart of top 10 fastest countries to vaccinate 50%
plt.figure(figsize=(12, 6))
vacc_speed.plot(kind='bar', color='green')
plt.title('Top 10 Countries: Fastest to Vaccinate 50% of Population')
plt.ylabel('Days to Reach 50% Vaccination')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(
    'D:/Git/COVID-19-Data-Analysis/data/fastest_vaccination_countries.png')
