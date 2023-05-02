#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:41:02 2023

@author: carlessansfuentes
"""
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta, date
import itertools




######### 1. DATA CREATION
# Define the list of cities
cities = ['Tokyo', 'Delhi', 'Shanghai', 'Sao Paulo', 'Mexico City', 'Cairo', 'Mumbai', 'Beijing', 'Dhaka', 'Osaka',
          'New York City', 'Karachi', 'Buenos Aires', 'Chongqing', 'Istanbul', 'Kolkata', 'Manila', 'Lagos', 'Rio de Janeiro', 
          'Tianjin', 'Kinshasa', 'Guangzhou', 'Los Angeles', 'Moscow', 'Shenzhen', 'Lahore', 'Bangalore', 'Paris', 'Bogotá',
          'Jakarta', 'Chennai', 'Lima', 'Bangkok', 'Hyderabad', 'London', 'Ljubljana', 'Nanjing', 'Wuhan', 'Ho Chi Minh City',
          'Luanda', 'Ahmedabad', 'Kuala Lumpur', 'Harbin', 'Hong Kong', 'Houston', 'Montreal', 'Santiago', 'Saint Petersburg',
          'Madrid', 'Pune', 'Singapore', 'Washington, D.C.', 'Surat', 'Kabul', 'Johannesburg', 'Kanpur', 'Nagoya', 'Yangon', 'Chittagong',
          'Alexandria', 'Shenyang', 'Qingdao', 'Baghdad', 'Tehran', 'Hanoi', 'Riyadh', 'Rome', 'Dubai', 'Sydney', 'Ankara', 'Taipei', 
          'Dar es Salaam', 'Tashkent', 'Belo Horizonte', 'Singapore', 'Jeddah', 'Nairobi', 'Calgary', 'Casablanca', 'Abidjan', 'Curitiba', 
          'Nanjing', 'San Francisco', 'Fortaleza', 'Haifa', 'Baku', 'Budapest', 'Kampala', 'Gujranwala', 'Minsk', 'Warsaw', 'Kazan', 
          'Rabat', 'Toronto', 'Belgrade', 'Surabaya', 'Houston', 'Zhengzhou', 'Guayaquil', 'Lyon', 'Beirut', 'Madrid', 'Manaus', 'Medellín', 
          'Melbourne', 'Barcelona', 'Brisbane', 'Chicago', 'Porto Alegre', 'Durban', 'Sofia']

# Define the initial and end dates for each city
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 1)

# Create an empty list to store the data for each city
data = []

# Loop over the cities and generate a random initial date and end date
for i in range(1000):
    city = random.choice(cities)
    initial_date = start_date + timedelta(days=random.randint(0, 1064))
    end_date = initial_date + timedelta(days=100)
    data.append([city, initial_date, end_date])

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data, columns=['city', 'initial_date', 'end_date'])
df.head(5)

df_cityplans = df.groupby("city").size().reset_index(name="n_city").sort_values(by = "n_city",ascending=False)
######### 2. DATA WRANGLING AND INTERSECTION CALCULATION
# Display the DataFrame
def has_overlap(a_start, a_end, b_start, b_end, min_days_intersect=2):
    """

    Parameters
    ----------
    a_start : timestamp
        start_date at place a
    a_end : TYPE
        end_date at place a.
    b_start : TYPE
        start_date at place b.
    b_end : TYPE
        end_date at place b.
    min_days_intersect : int, optional
        it is the minimum number of days for intersection be considered. The default is 2. 
        That means that less than 2 days intersection does not account for intersection

    Returns
    -------
    Boolen
        True if intersects, False otherwise.

    """
    latest_start = max(a_start, b_start)
    earliest_end = min(a_end, b_end)
    
    return latest_start+timedelta(days=2) <= earliest_end
    # d1 = date(2000, 1, 10)
    # d2 = date(2000, 1, 11)
    # d3 = date(2000, 1, 15)
    # d4 = date(2000, 1, 15)
    #has_overlap(d1,d2,d3,d4)



def get_number_of_intersections_by_city(df, city):
    # Subset dataframe by city
    df_city = df[df.city == city].reset_index(drop=True)

    # Create list of all pairwise combinations of rows in the dataframe
    n_rows = df_city.shape[0]
    combinations = list(itertools.combinations(range(n_rows), 2))
    total_n_intersection =len(combinations)

    # Count the number of intersections for each pairwise combination of rows
    n_intersects_bycities = [has_overlap(df_city.initial_date[row_i], df_city.end_date[row_i],
                                         df_city.initial_date[row_j], df_city.end_date[row_j])
                            for row_i, row_j in combinations]

    # Append the total number of intersections for the city to the list
    return total_n_intersection, sum(n_intersects_bycities) 

    # Create a new dataframe with the total number of intersections for each city

city = "Madrid"
df_city = df[df.city == city].reset_index(drop=True)

get_number_of_intersections_by_city(df, "Madrid")

unique_cities = df.city.unique()
n_total_intersects=[]
n_intersects = []

for city in unique_cities:
    total_n_intersection_city, n_intersects_city = get_number_of_intersections_by_city(df, city)
    n_total_intersects.append(total_n_intersection_city)
    n_intersects.append(n_intersects_city)


data = {'city': unique_cities, 'total_possible_intersections':n_total_intersects ,'n_intersects': n_intersects}
final_df = pd.DataFrame(data).sort_values(by="n_intersects", ascending=False).reset_index(drop=True)



df =df_cityplans.merge(final_df, how="outer", on = "city")


### 3. VISUALIZATION IN STREAMLIT

# Add sidebar to filter by value
with st.sidebar:
    st.title("Filter and Sort Options")
    column = st.selectbox("Select a column", df.columns[1:])
    operation = st.selectbox("Select an operation", [">", "<"])
    value = st.number_input(f"Enter the {column} value", value=0)
    sort_column = st.selectbox("Select a column for sorting", df.columns[1:])

# Filter the DataFrame based on the selected options
if operation == ">":
    filtered_df = df.loc[df[column] > value]
else:
    filtered_df = df.loc[df[column] < value]

# Sort the filtered DataFrame by the selected column
sorted_df = filtered_df.sort_values(sort_column)

# Display the filtered and sorted DataFrame
st.write(f"Filtered and sorted DataFrame ({operation} {value} for column {column}, sorted by {sort_column}):")
st.write(sorted_df)