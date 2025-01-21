import csv
import pandas as pd


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

#adds the combind datasets to a csv file
combined_df.to_csv("cleaned_up_data.csv", index=False)

#list comprehention coverting floats to ints
file = open("cleaned_up_data.csv","r")
myList = file.read()
reader = csv.DictReader(file)
myList.split(",")
death_data = [row['total_deaths']for row in reader ]
processed_data =[int(value)for value in death_data if value.isdigit()]
print(processed_data)

case_data = [row['total_cases']for row in reader ]
processed_data =[int(value)for value in case_data if value.isdigit()]
print(processed_data)

#finding the max cases
target_row_index = 2
row_values = df.iloc[target_row_index]
max_value = row_values.max()
print(max_value)

file.close()
