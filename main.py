import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='white', palette='Pastel2')

def read_file(filepath, plot=True):
    file = pd.read_csv(filepath, header=1)
    df = file.set_index('Week').stack().reset_index()
    df.columns = ['week', 'region', 'interest']
    df['week'] = pd.to_datetime(df['week'])
    plt.figure(figsize=(8, 3))
    df = df[df['interest'] != "<1"]
    df['interest'] = pd.to_numeric(df['interest'], errors='coerce')  # Convert 'interest' to numeric

    if plot:
        sns.lineplot(data=df, x='week', y='interest', hue='region')
    return df

# Now, when performing aggregation:
workout = read_file('workout.csv')
workout['interest'] = pd.to_numeric(workout['interest'], errors='coerce')

# Group by month and calculate mean interest for each month
workout['month'] = workout['week'].dt.to_period('M')  # Create a new 'month' column
monthly_mean = workout.groupby('month')['interest'].mean()

# Find the month with the highest mean interest
max_mean_interest = monthly_mean.idxmax()
month_str = str(max_mean_interest.to_timestamp().date())

def read_geo(filepath, multi=False):
    """
    Reads a CSV file from a given filepath, converts it into a pandas DataFrame,
    and returns a processed DataFrame with columns: 'country', 'interest'.
    Generates a bar plot using Seaborn to visualize the data.
    """
    file = pd.read_csv(filepath, header=1)

    if not multi:
        file.columns = ['country', 'interest']
        plt.figure(figsize=(8, 4))
        sns.barplot(data=file.dropna().iloc[:25, :], y='country', x='interest')

    if multi:
        plt.figure(figsize=(3, 8))
        file = file.set_index('Country').stack().reset_index()
        file.columns = ['country', 'category', 'interest']
        file['interest'] = pd.to_numeric(file['interest'].apply(lambda x: x[:-1]))
        sns.barplot(data=file.dropna(), y='country', x='interest', hue='category')

    file = file.sort_values(ascending=False, by='interest')
    return file

workout_global = read_geo('workout_global.csv')
top_25_countries = workout_global.head(25)
top_country = top_25_countries['country'].iloc[0]

geo_categories = read_geo('geo_three_keywords.csv', multi=True)
MESA_countries = ["Philippines", "Singapore", "United Arab Emirates", "Qatar", "Kuwait",
                  "Malaysia", "Sri Lanka", "India", "Pakistan", "Lebanon"]
MESA = geo_categories.loc[geo_categories.country.isin(MESA_countries), :]

MESA_pivot = MESA.set_index(['country', 'category']).unstack()
top_home_workout_country = 'Philippines'

read_file('yoga_zumba_sng.csv')
read_file('yoga_zumba_phl.csv')
pilot_content = ['yoga', 'zumba']

plt.show()
