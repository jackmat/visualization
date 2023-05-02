#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 13:32:43 2023

@author: carlessansfuentes
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:41:02 2023

@author: carlessansfuentes
"""
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import itertools
import time
from tqdm import tqdm


######### 1. DATA CREATION
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

start_date = datetime(2022, 1, 1)

data = []

for _ in range(10000):
    city = random.choice(cities)
    initial_date = start_date + timedelta(days=random.randint(0, 1064))
    end_date = initial_date + timedelta(days=100)
    data.append([city, initial_date, end_date])

df = pd.DataFrame(data, columns=['city', 'initial_date', 'end_date'])
print(df)
######### 2. DATA WRANGLING AND INTERSECTION CALCULATION
def has_overlap(a_start, a_end, b_start, b_end, min_days_intersect=2):
    latest_start = max(a_start, b_start)
    earliest_end = min(a_end, b_end)
    return latest_start + timedelta(days=min_days_intersect) <= earliest_end

def get_number_of_intersections_by_city(df, city):
    df_city = df[df.city == city].reset_index(drop=True)
    n_rows = df_city.shape[0]
    combinations = list(itertools.combinations(range(n_rows), 2))

    return sum(has_overlap(df_city.initial_date[row_i], df_city.end_date[row_i],
                            df_city.initial_date[row_j], df_city.end_date[row_j])
               for row_i, row_j in combinations)


start_time = time.time()
unique_cities = df.city.unique()
start_time = time.time()

unique_cities = df.city.unique()
n_intersects = []
for city in tqdm(unique_cities):
    n_intersects.append(get_number_of_intersections_by_city(df, city))

final_df = pd.DataFrame({'city': unique_cities, 'n_intersects': n_intersects})
final_df.sort_values(by="n_intersects", ascending=False, inplace=True)
final_df.reset_index(drop=True, inplace=True)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time/60:.2f} minutes")



######### 3. VISUALIZATION IN STREAMLIT
filter_value = st.sidebar.number_input('Filter value', value=0)
filtered_df = final_df.query('n_intersects > @filter_value')
st.dataframe(filtered_df)