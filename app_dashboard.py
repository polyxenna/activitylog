import pandas as pd
import plotly.express as px
import streamlit as st



st.set_page_config(layout="centered", initial_sidebar_state="expanded")
# Import custom CSS file
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)
# Load the dataset
df = pd.read_csv('activity_log.csv')

#SIDEBAR

st.sidebar.header("Activity Log")

# Create sidebar with buttons to show specific plots
option = st.sidebar.selectbox('Select a plot', ('Amount of Sleep Per Day', 'Location of Time Spent', 'Time Spent per Activity Type', 'Average Time Spent on Commute per Day', 'Number of Times That I Eat per Day', 'Number of Times That I Eat Each Type of Meal', 'Trend of High Productivity Instances Over Time (School Related Work)', 'Distribution of my Feelings over the Past 2 Weeks'))

st.sidebar.markdown('''
---
Created by Bianca Jessa A. Carabio BSIT - G1
                                        ''')
# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Convert 'Duration' column to timedelta format
df['Duration'] = pd.to_timedelta(df['Duration'])

if option == 'Amount of Sleep Per Day':
    # Filter out rows where 'Activity' is not 'Sleep'
    sleep_df = df[df['Activity'] == 'Sleep']

    # Group by 'Date' and sum 'Duration'
    sleep_per_day = sleep_df.groupby('Date')['Duration'].sum()

    # Reset index to make 'Date' a column again
    sleep_per_day = sleep_per_day.reset_index()

    # Convert 'Duration' to hours for easier interpretation
    sleep_per_day['Duration'] = sleep_per_day['Duration'].dt.total_seconds() / 3600

    # Calculate average amount of sleep
    average_sleep = sleep_per_day['Duration'].mean()

    # Add markdown to explain the plot
    st.markdown(f"### Amount of Sleep Per Day for 2 Weeks\n\nThis plot shows the amount of sleep I had per day for the past 2 weeks.\n\n")

    # Plot line chart
    fig2 = px.line(sleep_per_day, x='Date', y='Duration', title='Amount of Sleep Per Day for 2 Weeks')
    fig2.update_layout(xaxis_title='Date', yaxis_title='Sleep in Hours', xaxis=dict(dtick='D1', tickformat='%b %d'))
    st.plotly_chart(fig2)

    # Add metric to show the average amount of sleep
    st.markdown(f'<div class="metric">Average Sleep: {average_sleep:.2f} hours</div>', unsafe_allow_html=True)

elif option == 'Location of Time Spent':
    # Group by 'Location' and sum 'Duration'
    time_spent = df.groupby('Location')['Duration'].sum()

    # Reset index to make 'Location' a column again
    time_spent = time_spent.reset_index()

    # Convert 'Duration' to hours for easier interpretation
    time_spent['Duration'] = time_spent['Duration'].dt.total_seconds() / 3600

    # Plot pie chart
    fig3 = px.pie(time_spent, values='Duration', names='Location', title='Location of Time Spent')
    st.plotly_chart(fig3)

elif option == 'Time Spent per Activity Type':
    # Group by 'Activity Type' and sum 'Duration'
    activity_type_df = df.groupby('Activity Type')['Duration'].sum()

    # Reset index to make 'Activity Type' a column again
    activity_type_df = activity_type_df.reset_index()

    # Convert 'Duration' to hours for easier interpretation
    activity_type_df['Duration'] = activity_type_df['Duration'].dt.total_seconds() / 3600

    # Plot pie chart
    fig4 = px.pie(activity_type_df, values='Duration', names='Activity Type', title='Time Spent per Activity Type')
    st.plotly_chart(fig4)

elif option == 'Average Time Spent on Commute per Day':
    # Filter out rows where 'Activity' is not 'Commute'
    commute_df = df[df['Activity'] == 'Commute']

    # Group by 'Date' and sum 'Duration'
    commute_per_day = commute_df.groupby('Date')['Duration'].sum()

    # Reset index to make 'Date' a column again
    commute_per_day = commute_per_day.reset_index()

    # Convert 'Duration' to hours for easier interpretation
    commute_per_day['Duration'] = commute_per_day['Duration'].dt.total_seconds() / 3600

    # Calculate average commute time
    average_commute = commute_per_day['Duration'].mean()

    # Plot bar chart
    fig5 = px.bar(commute_per_day, x='Date', y='Duration', title='Average Time Spent on Commute per Day')
    fig5.update_layout(xaxis_title='Date', yaxis_title='Time in Hours', xaxis=dict(dtick='D1', tickformat='%b %d'))
    st.plotly_chart(fig5)

elif option == 'Number of Times That I Eat per Day':
    # Filter out rows where 'Activity' does not contain 'Eat'
    if df["Activity"].isna().any():
        eat_df = df.dropna(subset=["Activity"])
    else:
        eat_df = df.copy()

    eat_df = eat_df[eat_df["Activity"].str.contains("Eat")]

    # Count the number of times you eat each day
    eat_per_day = eat_df.groupby('Date').size()

    # Reset index to make 'Date' a column again
    eat_per_day = eat_per_day.reset_index()

    # Rename the count column to 'Times'
    eat_per_day.columns = ['Date', 'Times']

    # Plot bar chart
    fig6 = px.bar(eat_per_day, x='Date', y='Times', title='Number of Times That I Eat per Day')
    fig6.update_layout(xaxis_title='Date', yaxis_title='Count', xaxis=dict(dtick='D1', tickformat='%b %d'))
    st.plotly_chart(fig6)

elif option == 'Number of Times That I Eat Each Type of Meal':
    # Filter out rows where 'Activity' does not contain 'Eat'
    eat_df = df.dropna(subset=["Activity"])
    eat_df = eat_df[eat_df["Activity"].str.contains("Eat")]

    # Count the number of times you eat each type of meal each day
    meal_counts = eat_df['Activity'].value_counts()

    # Reset index to make 'Activity' a column again
    meal_counts = meal_counts.reset_index()

    # Rename the columns to 'Meal' and 'Count'
    meal_counts.columns = ['Meal', 'Count']

    # Plot pie chart
    fig7 = px.pie(meal_counts, values='Count', names=meal_counts['Meal'].str.replace('Eat ', ''), title='Number of Times That I Eat Each Type of Meal')
    st.plotly_chart(fig7)

elif option == 'Trend of High Productivity Instances Over Time (School Related Work)':
    # Filter out rows where 'Value' is not 'High' and 'Activity Type' is not 'School'
    productive_df = df[(df['Value'] == 'High') & (df['Activity Type'] == 'School')]

    # Count the number of high productivity instances each day
    productive_per_day = productive_df.groupby('Date').size()

    # Reset index to make 'Date' a column again
    productive_per_day = productive_per_day.reset_index()

    # Rename the count column to 'Count'
    productive_per_day.columns = ['Date', 'Count']

    # Plot line chart
    fig11 = px.line(productive_per_day, x='Date', y='Count', title='Trend of High Productivity Instances Over Time (School Related Work)')
    fig11.update_layout(xaxis_title='Date', yaxis_title='Count', xaxis=dict(dtick='D1', tickformat='%b %d'))
    st.plotly_chart(fig11)

elif option == 'Distribution of my Feelings over the Past 2 Weeks':
    # Group by 'How I Feel' and count the number of instances of each feeling
    feelings_counts = df.groupby('How I feel').size()

    # Reset index to make 'How I Feel' a column again
    feelings_counts = feelings_counts.reset_index()

    # Rename the count column to 'Count'
    feelings_counts.columns = ['Feeling', 'Count']

    # Sort by 'Count' column in descending order
    feelings_counts = feelings_counts.sort_values(by='Count', ascending=False)

    # Plot histogram
    fig12 = px.histogram(feelings_counts, x='Feeling', y='Count', title='Distribution of my Feelings over the Past 2 Weeks')
    st.plotly_chart(fig12)