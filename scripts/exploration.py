import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Check distribution of promotions in training and test sets
def check_promo_distribution(train_df, test_df):
  train_promo_dist = train_df['Promo'].value_counts(normalize=True)
  test_promo_dist = test_df['Promo'].value_counts(normalize=True)
  print("Train Promo Distribution:")
  print(train_promo_dist)
  print("\nTest Promo Distribution:")
  print(test_promo_dist)
  sns.barplot(x=train_promo_dist.index, y=train_promo_dist.values, alpha=0.7, label='Train')
  sns.barplot(x=test_promo_dist.index, y=test_promo_dist.values, alpha=0.7, label='Test')
  plt.legend()
  plt.title('Promo Distribution in Train vs Test Sets')
  plt.show()
  
# 2. Check & compare sales behavior around holidays
def analyze_holiday_sales(data, holiday_column):
  # Ensure the 'Date' column is in datetime format
  data['Date'] = pd.to_datetime(data['Date'])
  
  # Filter holidays
  holidays = data[data[holiday_column] == 1]
  
  if holidays.empty:
    print("No holidays found in the data.")
    return

  # Get the dates of holidays
  holiday_dates = holidays['Date'].unique()
  
  # Define the periods around holidays
  before_holidays = data[(data['Date'].isin(holiday_dates - pd.Timedelta(days=7))) | 
              (data['Date'].isin(holiday_dates - pd.Timedelta(days=6))) |
              (data['Date'].isin(holiday_dates - pd.Timedelta(days=5))) |
              (data['Date'].isin(holiday_dates - pd.Timedelta(days=4))) |
              (data['Date'].isin(holiday_dates - pd.Timedelta(days=3))) |
              (data['Date'].isin(holiday_dates - pd.Timedelta(days=2))) |
              (data['Date'].isin(holiday_dates - pd.Timedelta(days=1)))]

  after_holidays = data[(data['Date'].isin(holiday_dates + pd.Timedelta(days=1))) |
               (data['Date'].isin(holiday_dates + pd.Timedelta(days=2))) |
               (data['Date'].isin(holiday_dates + pd.Timedelta(days=3))) |
               (data['Date'].isin(holiday_dates + pd.Timedelta(days=4))) |
               (data['Date'].isin(holiday_dates + pd.Timedelta(days=5))) |
               (data['Date'].isin(holiday_dates + pd.Timedelta(days=6))) |
               (data['Date'].isin(holiday_dates + pd.Timedelta(days=7)))]

  # Calculate average sales
  sales_data = {
    'Before Holidays': before_holidays['Sales'].mean() if not before_holidays.empty else 0,
    'During Holidays': holidays['Sales'].mean(),
    'After Holidays': after_holidays['Sales'].mean() if not after_holidays.empty else 0
  }
  
  # Plotting the results
  sns.barplot(x=list(sales_data.keys()), y=list(sales_data.values()))
  plt.title('Sales Behavior Around Holidays')
  plt.ylabel('Average Sales')
  plt.show()

# 3. Seasonal purchase behavior
def analyze_seasonal_behavior(data, season_column):
  seasonal_sales = data.groupby(season_column)['Sales'].mean()
  sns.barplot(x=seasonal_sales.index, y=seasonal_sales.values)
  plt.title('Seasonal Purchase Behavior')
  plt.ylabel('Average Sales')
  plt.show()

# 4. Correlation between sales and number of customers
def correlation_sales_customers(data):
  correlation = data['Sales'].corr(data['Customers'])
  print(f"Correlation between Sales and Customers: {correlation}")
  sns.scatterplot(x='Customers', y='Sales', data=data)
  plt.title('Sales vs. Customers')
  plt.show()

# 5. Effect of promos on sales and customer attraction
def analyze_promo_effect(data):
  promo_sales = data[data['Promo'] == 1]['Sales'].mean()
  no_promo_sales = data[data['Promo'] == 0]['Sales'].mean()
  
  promo_customers = data[data['Promo'] == 1]['Customers'].mean()
  no_promo_customers = data[data['Promo'] == 0]['Customers'].mean()
  
  print(f"Sales with Promo: {promo_sales}, Sales without Promo: {no_promo_sales}")
  print(f"Customers with Promo: {promo_customers}, Customers without Promo: {no_promo_customers}")

# 6. Effective promo deployment
def promo_deployment_analysis(data):
  promo_effectiveness = data.groupby('Store')['Promo'].mean()
  stores_with_high_promo_effect = promo_effectiveness.sort_values(ascending=False).head(10)
  print("Stores with highest promo effectiveness:")
  print(stores_with_high_promo_effect)
    
# 7. Trends during store opening and closing times
def customer_behavior_open_close(data):
  # Group by 'Open' status and calculate average number of customers
  average_customers = data.groupby('Open')['Customers'].mean().reset_index()

  # Plot the results
  plt.figure(figsize=(8, 5))
  sns.barplot(x='Open', y='Customers', data=average_customers)
  plt.title('Average Number of Customers Based on Store Open Status')
  plt.xlabel('Store Open (1 = Open, 0 = Closed)')
  plt.ylabel('Average Number of Customers')
  plt.xticks([0, 1], ['Closed', 'Open'])  # Label the x-ticks
  plt.show()

# 8. Stores open on all weekdays and their weekend sales
def weekday_open_analysis(data):
  weekday_open = data.groupby('Store')['Open'].sum()
  all_week_open_stores = weekday_open[weekday_open >= 7]
  weekend_sales = data[(data['Store'].isin(all_week_open_stores.index)) & (data['DayOfWeek'] > 5)]['Sales'].mean()
  print(f"Average weekend sales for stores open all weekdays: {weekend_sales}")

# 9. Effect of assortment type on sales
def assortment_type_analysis(data):
  assortment_sales = data.groupby('Assortment')['Sales'].mean()
  sns.barplot(x=assortment_sales.index, y=assortment_sales.values)
  plt.title('Effect of Assortment Type on Sales')
  plt.ylabel('Average Sales')
  plt.show()

# 10. Distance to competitor and its effect on sales
def competitor_distance_analysis(data):
  sns.scatterplot(x='CompetitionDistance', y='Sales', data=data)
  plt.title('Effect of Competition Distance on Sales')
  plt.xlabel('Competition Distance')
  plt.ylabel('Sales')
  plt.show()

# 11. Effect of opening/reopening competitors
def analyze_new_competitors(data):
  # Ensure the 'Date' column is in datetime format
  data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
  
  # Filter stores with new competitors
  new_competitors = data[data['CompetitionOpenSinceYear'].notna() & data['CompetitionOpenSinceMonth'].notna()]
  
  if new_competitors.empty:
    print("No new competitors found in the data.")
    return
  
  # Calculate the date when the competition opened
  new_competitors['CompetitionOpenDate'] = pd.to_datetime(
    new_competitors['CompetitionOpenSinceYear'].astype(int).astype(str) + '-' +
    new_competitors['CompetitionOpenSinceMonth'].astype(int).astype(str) + '-01'
  )
  
  # Get the minimum competition open date
  competition_open_date = new_competitors['CompetitionOpenDate'].min()
  
  # Filter data for the period before and after the competition opened
  before_competition = data[data['Date'] < competition_open_date]
  after_competition = data[data['Date'] >= competition_open_date]
  
  # Ensure there are sales data points before and after competition
  if before_competition.empty or after_competition.empty:
    print("No sales data available before or after competition.")
    return
  
  # Calculate average sales before and after competition
  sales_data = {
    'Before Competition': before_competition['Sales'].mean(),
    'After Competition': after_competition['Sales'].mean() if not after_competition.empty else 0
  }
  
  # Ensure average sales before competition is not zero
  if sales_data['Before Competition'] == 0:
    print("Average sales before competition is zero. Adjusting to a minimum sales value.")
    sales_data['Before Competition'] = 1  # Set to a small default value if needed
  
  # Plotting the results
  sns.barplot(x=list(sales_data.keys()), y=list(sales_data.values()))
  plt.title('Sales Before and After New Competitors')
  plt.ylabel('Average Sales')
  plt.show()

# 12. Effect of opening/reopening competitors with NA competitor distance
def analyze_competitor_distance_effect(data):
  # Ensure the 'Date' column is in datetime format
  data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
  
  # Filter stores with NA competitor distance initially and later have values
  stores_with_na_distance = data[data['CompetitionDistance'].isna()]['Store'].unique()
  stores_with_distance = data[data['Store'].isin(stores_with_na_distance) & data['CompetitionDistance'].notna()]
  
  if stores_with_distance.empty:
    print("No stores found with NA competitor distance initially and later have values.")
    return
  
  # Get the date when the competitor distance was first recorded
  stores_with_distance['FirstRecordedDate'] = stores_with_distance.groupby('Store')['Date'].transform('min')
  
  # Filter data for the period before and after the competitor distance was recorded
  before_distance = data[data['Date'] < stores_with_distance['FirstRecordedDate'].min()]
  after_distance = data[data['Date'] >= stores_with_distance['FirstRecordedDate'].min()]
  
  # Ensure there are sales data points before and after competitor distance was recorded
  if before_distance.empty or after_distance.empty:
    print("No sales data available before or after competitor distance was recorded.")
    return
  
  # Calculate average sales before and after competitor distance was recorded
  sales_data = {
    'Before Distance Recorded': before_distance['Sales'].mean(),
    'After Distance Recorded': after_distance['Sales'].mean() if not after_distance.empty else 0
  }
  
  # Plotting the results
  sns.barplot(x=list(sales_data.keys()), y=list(sales_data.values()))
  plt.title('Sales Before and After Competitor Distance Recorded')
  plt.ylabel('Average Sales')
  plt.show()