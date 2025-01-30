import csv
import pandas as pd
import matplotlib.pyplot as plt

DATA_URL = "https://raw.githubusercontent.com/owid/monkeypox/refs/heads/main/owid-monkeypox-data.csv"
df = pd.read_csv(DATA_URL)
# Filter data for the spain.
spain_df = df[df['iso_code'] == 'ESP']

DATA_URL = "https://raw.githubusercontent.com/owid/monkeypox/refs/heads/main/owid-monkeypox-data.csv"
df = pd.read_csv(DATA_URL)
# Filter data for the United kigdom
uk_df = df[df['iso_code'] == 'GBR']

#main columns
columns_of_intrest = ['location','total_cases','total_deaths','date']
uk_df=uk_df[columns_of_intrest]
spain_df= spain_df[columns_of_intrest]
#cleans the data 
spain_df = spain_df.dropna()
uk_df = uk_df.dropna()

#combines both datasets
combined_df = pd.concat([spain_df, uk_df])


# Convert date to Year-Month format for aggregation
combined_df['date'] = pd.to_datetime(combined_df['date'])  # Ensure datetime format
combined_df['Year-Month'] = combined_df['date'].dt.to_period('M')  # Convert to YYYY-MM

# Aggregate data by month
monthly_data = combined_df.groupby(['location', 'Year-Month']).sum().reset_index()

# Save to CSV
monthly_data.to_csv("monthly_cleaned_data.csv", index=False)

#adds the combind datasets to a csv file
combined_df.to_csv("cleaned_up_data.csv", index=False)

#list comprehention coverting floats to ints
file = open("monthly_cleaned_data.csv","r")
myList = file.read()
reader = csv.DictReader(file)
myList.split(",")
# Open the CSV file
with open("monthly_cleaned_data.csv", "r") as file:
    reader = csv.DictReader(file)
    
    # Extract and process death data
    death_data = [row['total_deaths'] for row in reader if row['total_deaths']]
    processed_death_data = [float(value) for value in death_data if value.replace('.', '', 1).isdigit()]
    print("Processed Death Data:", processed_death_data)

# Reopen the file for case data, since the reader has been consumed
with open("monthly_cleaned_data.csv", "r") as file:
    reader = csv.DictReader(file)
    
    # Extract and process case data. used list coprihention to convert the data.
    case_data = [row['total_cases'] for row in reader if row['total_cases']]
    processed_case_data = [float(value) for value in case_data if value.replace('.', '', 1).isdigit()]
    print("Processed Case Data:", processed_case_data)
    
     # Extract and process case data. used list coprihention to convert the data.
    month_data = [row['year-month'] for row in reader if row['total_cases']]
    print(month_data)
#finding the max cases
# target_row_index = 2
# row_values = df.iloc[target_row_index]
# max_value = row_values.max()
#print(max_value)
maxValueD = max(processed_death_data)
print(maxValueD)
maxValueC = max(processed_case_data)
print(maxValueC)

#print(min_values)
minValueD = min(processed_death_data)
print(minValueD)
minValueC = min(processed_case_data)
print(minValueC)

#total deaths
sumValueD = 0
for i in processed_death_data:
    sumValueD += i
print(sumValueD)

#total cases
sumValueC = 0
for i in processed_case_data:
    sumValueC += i
print(sumValueC)

#death averrage
averageD = sumValueD/len(processed_death_data)
averageD = round(averageD,2)
print(averageD)

#cases average
averageC = sumValueC/len(processed_case_data)
averageC = round(averageC,2)
print(averageC)



# Create figure and axis
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot total cases on primary y-axis
ax1.plot(month_data, processed_case_data, color='blue', marker='o', label="Total Cases")
ax1.set_xlabel("Time (Year-Month)")
ax1.set_ylabel("Total Cases", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create secondary y-axis
ax2 = ax1.twinx()
ax2.plot(month_data, processed_death_data, color='red', marker='s', label="Total Deaths")
ax2.set_ylabel("Total Deaths", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Title and layout
plt.title("Total Cases and Total Deaths Over Time")
fig.tight_layout()
plt.show()
# plt.plot(processed_death_data)
# plt.plot(processed_case_data)
# plt.show()

file.close()

