import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

datetime_columns = ["dteday"]

for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])

datetime_columns = ["dteday"]

for column in datetime_columns:
  hour_df[column] = pd.to_datetime(hour_df[column])

# Mengubah musim menjadi tipe kategori
columns = ['season', 'mnth', 'weekday', 'weathersit', 'holiday']

# konversi menjadi tipe kategori
for column in columns:
    day_df[column] = day_df[column].astype('category')
    hour_df[column] = day_df[column].astype('category')

day_df.rename(columns={
    'instant':'Instant',
    'dteday':'Date_day',
    'season':'Season',
    'yr':'Year',
    'mnth':'Month',
    'holiday':'Holiday',
    'weekday':'Weekday',
    'weathersit':'Weather_situation',
    'windspeed':'Wind_speed',
    'cnt':'Count_cr',
    'hum':'Humidity'
}, inplace=True)

day_df.head()

hour_df.rename(columns={
    'instant':'Instant',
    'dteday':'Date_day',
    'season':'Season',
    'hr': 'Hour',
    'yr' : 'Year',
    'mnth':'Month',
    'holiday':'Holiday',
    'weekday':'Weekday',
    'weathersit':'Weather_situation',
    'windspeed':'Wind_speed',
    'cnt':'Count_cr',
    'hum':'Humidity'
}, inplace=True)

hour_df.head()

#replace season
season_dict = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

day_df['Season'] = day_df['Season'].map(season_dict)
hour_df['Season'] = hour_df['Season'].map(season_dict)

#replace month
month_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

day_df['Month'] = day_df['Month'].map(month_dict)
hour_df['Month'] = hour_df['Month'].map(month_dict)

#replace holiday
holiday_dict = {
    0: 'No',
    1: 'Yes'
}

day_df['Holiday'] = day_df['Holiday'].map(holiday_dict)
hour_df['Holiday'] = hour_df['Holiday'].map(holiday_dict)

#replace weekday
weekday_dict = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}

day_df['Weekday'] = day_df['Weekday'].map(weekday_dict)
hour_df['Weekday'] = hour_df['Weekday'].map(weekday_dict)

#replace weather
weather_dict = {
    1: 'Clear',
    2: 'Mist',
    3: 'Light Snow',
    4: 'Heavy Rain'
}

day_df['Weather_situation'] = day_df['Weather_situation'].map(weather_dict)
hour_df['Weather_situation'] = hour_df['Weather_situation'].map(weather_dict)

#replace year
year_dict = {
    0: '2011',
    1: '2012'
}

day_df['Year'] = day_df['Year'].map(year_dict)
hour_df['Year'] = hour_df['Year'].map(year_dict)

day_df.drop(['workingday'], axis = 1, inplace= True)
hour_df.drop(['workingday'], axis = 1, inplace= True)

def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="Year").agg({"Count_cr": ["sum"]})
    return hour_count_df

def get_total_count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('Date_day >= "2011-01-01" and Date_day < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="Date_day").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="Date_day").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("Year").Count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def kind_of_season (day_df): 
    season_df = day_df.groupby(by="Season").Count_cr.sum().reset_index() 
    return season_df

days_df = pd.read_csv("day_data.csv")
hours_df = pd.read_csv("hour_data.csv")

datetime_columns = ["Date_day"]
days_df.sort_values(by="Date_day", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="Date_day", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["Date_day"].min()
max_date_days = days_df["Date_day"].max()

min_date_hour = hours_df["Date_day"].min()
max_date_hour = hours_df["Date_day"].max()

with st.sidebar:
    #For logo or image
    st.image("https://cdn.pixabay.com/photo/2014/07/05/08/18/bicycle-384566_1280.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
    
main_df_days = days_df[(days_df["Date_day"] >= str(start_date)) & 
                       (days_df["Date_day"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["Date_day"] >= str(start_date)) & 
                        (hours_df["Date_day"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = get_total_count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = kind_of_season(main_df_hour)

#Completing dashborad with data visualisation
st.header('Bike Sharing by RA Corp :sparkles:')

st.subheader('Our Sharing Information')
col1, col2 = st.columns(2)
 
with col1:
    total_orders = day_df_count_2011.Count_cr.sum()
    st.metric("Total of Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total of Registered", value=total_sum)

st.subheader("Question 1: How do bicycle rent perform for each year?")
yearly_rentals = day_df.groupby("Year")["Count_cr"].sum()

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(yearly_rentals.index, yearly_rentals.values)
ax.set_xlabel("Year")
ax.set_ylabel("Total Rentals")
ax.set_title("Bicycle Rentals per Year")
ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig)

st.markdown("""
**Insight:**
- There was a significant increase in the total number of bicycle rentals from 2011 to 2012. The year 2011 recorded a total of around 1.25 million rentals, while in 2012 the number of rentals increased to more than 2 million.
- This rapid growth also indicates a wider market potential for bicycle rental-related businesses, such as bicycle accessories and other equipment.
- Looking at the increase in bicycle renters in 2012, there is an opportunity for further growth in the following year, especially in big cities.
""")

st.subheader("Question 2: In what month did bicycle rentals reach their highest target?")
monthly_rentals = day_df.groupby('Month', observed=False)['Count_cr'].sum().reset_index()

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthly_rentals['Month'] = pd.Categorical(monthly_rentals['Month'], categories=month_order, ordered=True)
monthly_rentals = monthly_rentals.sort_values('Month')

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(monthly_rentals['Month'].astype(str), monthly_rentals['Count_cr'])
ax.set_xlabel('Month')
ax.set_ylabel('Total Rentals')
ax.set_title('Total Bicycle Rentals per Month')
ax.set_xticklabels(monthly_rentals['Month'], rotation=45)

st.pyplot(fig)

st.markdown('''
**Insight:**
- It can be seen in the data visualization that bike rentals peak in the months between May and October. In August, rentals peak at close to 350,000 bike rentals.
- Months like January, February, and December have the lowest number of rentals, below 200,000 rentals. This could be due to unfavorable weather conditions, such as rain, snow, or cold temperatures, which make people cycle less often.
- Based on the data, this indicates that the better the weather conditions, the more people are encouraged to cycle more often.
''')

st.subheader("Question 3: (Cluestering) What are the patterns of bicycle use based on season and weather, and can they be grouped into several segments based on these patterns?")
pivot_table = pd.pivot_table(day_df, values='Count_cr', index='Season', columns='Weather_situation', aggfunc='mean', observed=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
ax.set_title('Average Number of Bicycle Rentals Based on Season and Weather')
ax.set_xlabel('Weather Conditions')
ax.set_ylabel('Seasons')

st.pyplot(fig)

st.markdown('''
**Interpretation of Results:**
- From the heatmap, it can be seen that in spring and autumn, the number of rentals tends to be higher when the weather is sunny.
- In summer, the number of rentals is also high when the weather is sunny, but decreases slightly when it is foggy.
- In winter, the number of rentals tends to be low, especially when the weather is rainy or snowy.
- We can group data into segments based on these patterns. For example, the "good weather" segment (spring, fall, summer with sunny weather), the "moderate weather" segment (summer with foggy), and the "bad weather" segment
(winter with rainy/snowy weather).
''')

st.subheader("Conclusion")
st.markdown('''
- There was a significant increase in the number of bicycle renters from 2011 to 2012.
- May - October are the months with the highest number of bicycle rentals, with the peak occurring in August.
- The lowest number of bicycle rentals occurs in January, February and December, possibly due to unfavorable weather conditions.
- Bicycle use patterns are influenced by season and weather. The number of rentals is high in spring and autumn when the weather is sunny, and in summer when the weather is sunny and slightly foggy.
- Rental numbers are low in the winter, especially when it rains or snows.
''')

st.caption('Copyright (c) Dicoding 2023')