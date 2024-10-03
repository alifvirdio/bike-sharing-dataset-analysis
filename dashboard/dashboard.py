import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def highest_lowest_season(day_dataframe):
    season_dataframe = day_dataframe.groupby("season")['count_total'].sum().sort_values(ascending=False).reset_index()
    season_rename = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season_dataframe['season'] = season_dataframe['season'].replace(season_rename)

    return season_dataframe

def total_user_month(day_dataframe):
    user_month_df = day_dataframe.groupby("month")['registered'].sum().reset_index()
    month_rename = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
        6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    user_month_df['month'] = user_month_df['month'].replace(month_rename)
    return user_month_df

def year_versus(day_dataframe):
    registered_user_df = day_dataframe.loc[:, ['year', 'month', 'registered']]

    ## Rename
    month_rename = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    registered_user_df['month'] = registered_user_df['month'].replace(month_rename)
    registered_user_df = registered_user_df.groupby(['year', 'month'])['registered'].sum().reset_index()

    ## Reorder Month
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    registered_user_df['month'] = pd.Categorical(registered_user_df['month'], categories=month_order, ordered=True)

    registered_user_df = registered_user_df.sort_values(by=['year', 'month']).reset_index(drop=True)

    month_abbrev = {
        'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
        'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
        'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
    }

    registered_user_df['month'] = registered_user_df['month'].replace(month_abbrev)

    return registered_user_df

# Load data
all_df = pd.read_csv('D:/KULIAHAJA/AnalisisDataPhyton/new_day.csv')

# Convert datetime columns
datetime_columns = ["date-day"]
all_df.sort_values(by="date-day", inplace=True)
all_df.reset_index(inplace=True, drop=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Input
highest_lowest = highest_lowest_season(all_df)
total_user = total_user_month(all_df)
year = year_versus(all_df)

# Header
st.header('Bike Sharing Dataset Analysis with Streamlit')

# Highest vs Lowest Season
st.subheader("Best and Worst Season for Bike Renting")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

colors = ["#ff4700", "#e5ff00", "#00ff59", "#00ffe3"]

sns.barplot(x="count_total", y="season", data=highest_lowest, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Season for Renting", loc="center", fontsize=20)
ax[0].tick_params(axis='y', labelsize=12)
ax[0].tick_params(axis='x', labelsize=12)

sns.barplot(x="count_total", y="season", data=highest_lowest.sort_values(by="count_total", ascending=True).head(4), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].set_title("Worst Season for Renting", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=12)
ax[1].tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# Total Registered User from 2011 to 2012
st.subheader("Total Registered Users 2011 to 2012")
fig, ax = plt.subplots(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Create the line plot with Seaborn
sns.lineplot(
    data=total_user,
    x="month",
    y="registered",
    marker='o',
    linewidth=2.5,
    color="#0006ff",
    ax=ax
)

# Enhancing the plot appearance
ax.set_title("Number of Registered Users per Month (2011-2012)", loc="center", fontsize=16, fontweight='bold')
ax.set_xlabel("Month", fontsize=12, fontweight='bold')
ax.set_ylabel("Number of Registered Users", fontsize=12, fontweight='bold')
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.grid(visible=True, linestyle='--', alpha=0.7)
st.pyplot(fig)

# 2011 vs 2012 Registered User per Month
st.subheader("2011 vs 2012 Registered User per Month")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=year, x='month', y='registered', hue='year', marker='o', palette='muted', linewidth=3.5, ax=ax)

ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Registered Users', fontsize=12, fontweight='bold')
ax.set_title('Total Registered Users by Month (2011 vs. 2012)', fontsize=16, fontweight='bold')
ax.legend(title='Year')
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--')
st.pyplot(fig)
