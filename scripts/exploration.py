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
