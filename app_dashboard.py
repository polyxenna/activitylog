import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
df = pd.read_csv('activity_log.csv')


############
# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Convert 'Duration' column to timedelta format
df['Duration'] = pd.to_timedelta(df['Duration'])

# Filter out rows where 'Activity' is not 'Sleep'
sleep_df = df[df['Activity'] == 'Sleep']

# Group by 'Date' and sum 'Duration'
sleep_per_day = sleep_df.groupby('Date')['Duration'].sum()

# Reset index to make 'Date' a column again
sleep_per_day = sleep_per_day.reset_index()

# Convert 'Duration' to hours for easier interpretation
sleep_per_day['Duration'] = sleep_per_day['Duration'].dt.total_seconds() / 3600

# Plot bar chart
fig1 = px.bar(sleep_per_day, x='Date', y='Duration', title='Amount of Sleep per Day (Bar Chart)')
st.plotly_chart(fig1)


########################
# Plot line chart
fig2 = px.line(sleep_per_day, x='Date', y='Duration', title='Amount of Sleep per Day (Line Chart)')
st.plotly_chart(fig2)


#########################
# Group by 'Location' and sum 'Duration'
time_spent = df.groupby('Location')['Duration'].sum()

# Reset index to make 'Location' a column again
time_spent = time_spent.reset_index()

# Convert 'Duration' to hours for easier interpretation
time_spent['Duration'] = time_spent['Duration'].dt.total_seconds() / 3600

# Plot pie chart
fig3 = px.pie(time_spent, values='Duration', names='Location', title='Time Spent per Location')
st.plotly_chart(fig3)

#########################
# Group by 'Activity Type' and sum 'Duration'
activity_type_df = df.groupby('Activity Type')['Duration'].sum()

# Reset index to make 'Activity Type' a column again
activity_type_df = activity_type_df.reset_index()

# Convert 'Duration' to hours for easier interpretation
activity_type_df['Duration'] = activity_type_df['Duration'].dt.total_seconds() / 3600

# Plot pie chart
fig4 = px.pie(activity_type_df, values='Duration', names='Activity Type', title='Time Spent per Activity Type')
st.plotly_chart(fig4)

#########################3
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
fig5 = px.bar(commute_per_day, x='Date', y='Duration', title='Average Commute Time per Day')
st.plotly_chart(fig5)

##################
# Filter out rows where 'Activity' does not contain 'Eat'
eat_df = df.dropna(subset=["Activity"])
eat_df = eat_df[eat_df["Activity"].str.contains("Eat")]

# Count the number of times you eat each day
eat_per_day = eat_df.groupby('Date').size()

# Reset index to make 'Date' a column again
eat_per_day = eat_per_day.reset_index()

# Rename the count column to 'Times'
eat_per_day.columns = ['Date', 'Times']

# Plot bar chart
fig6 = px.bar(eat_per_day, x='Date', y='Times', title='Number of Times Eating per Day')
st.plotly_chart(fig6)


##################
# Filter out rows where 'Activity' does not contain 'Eat'
if df["Activity"].isna().any():
    eat_df = df.dropna(subset=["Activity"])
else:
    eat_df = df.copy()

eat_df = eat_df[eat_df["Activity"].str.contains("Eat")]

# Count the number of times you eat each type of meal each day
meal_counts = eat_df['Activity'].value_counts()

# Reset index to make 'Activity' a column again
meal_counts = meal_counts.reset_index()

# Rename the columns to 'Meal' and 'Count'
meal_counts.columns = ['Meal', 'Count']

# Plot pie chart
fig7 = px.pie(meal_counts, values='Count', names='Meal', title='Number of Times Eating Each Meal')
st.plotly_chart(fig7)

##################
# Filter out rows where 'Value' is not 'High'
productive_df = df[df['Value'] == 'High']

# Count the number of high productivity instances each day
productive_per_day = productive_df.groupby('Date').size()

# Reset index to make 'Date' a column again
productive_per_day = productive_per_day.reset_index()

# Rename the count column to 'Count'
productive_per_day.columns = ['Date', 'Count']

# Plot bar chart
fig8 = px.bar(productive_per_day, x='Date', y='Count', title='Number of High Productivity Instances per Day')
st.plotly_chart(fig8)

# Plot line chart
fig9 = px.line(productive_per_day, x='Date', y='Count', title='Trend of High Productivity Instances Over Time')
st.plotly_chart(fig9)

#################
# Filter out rows where 'Value' is not 'High' and 'Activity Type' is not 'School'
productive_df = df[(df['Value'] == 'High') & (df['Activity Type'] == 'School')]

# Count the number of high productivity instances each day
productive_per_day = productive_df.groupby('Date').size()

# Reset index to make 'Date' a column again
productive_per_day = productive_per_day.reset_index()

# Rename the count column to 'Count'
productive_per_day.columns = ['Date', 'Count']

# Plot bar chart
fig10 = px.bar(productive_per_day, x='Date', y='Count', title='Number of High Productivity Instances per Day (School Work)')
st.plotly_chart(fig10)

# Plot line chart
fig11 = px.line(productive_per_day, x='Date', y='Count', title='Trend of High Productivity Instances Over Time (School Work)')
st.plotly_chart(fig11)
                
################
# Group certain activities together
df['Activity'] = df['Activity'].apply(lambda x: 'School Work/Class' if isinstance(x, str) and ('Class' in x or 'IT' in x or 'F2F' in x) else x)
df['Activity'] = df['Activity'].apply(lambda x: 'Meals' if isinstance(x, str) and ('Eat' in x) else x)
df['Activity'] = df['Activity'].apply(lambda x: 'Sleep' if isinstance(x, str) and ('Sleep' in x or 'Nap' in x or 'Rest' in x) else x)

# Count the frequency of each activity
activity_counts = df['Activity'].value_counts()

# Reset index to make 'Activity' a column again
activity_counts = activity_counts.reset_index()

# Rename the columns to 'Activity' and 'Count'
activity_counts.columns = ['Activity', 'Count']

# Keep only the top 5 activities and group the rest as 'Others'
top_activities = activity_counts.nlargest(5, 'Count')
other_activities = activity_counts.iloc[5:].sum(numeric_only=True)
other_activities['Activity'] = 'Others'
activity_counts = pd.concat([top_activities, other_activities.to_frame().T])

# Plot pie chart
fig12 = px.pie(activity_counts, values='Count', names='Activity', title='Frequency of Each Activity')
st.plotly_chart(fig12)