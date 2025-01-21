import csv
import pandas as pd


DATA_URL = "https://raw.githubusercontent.com/owid/monkeypox/refs/heads/main/owid-monkeypox-data.csv"
df = pd.read_csv(DATA_URL)
# Filter data for the United States
spain_df = df[df['iso_code'] == 'ESP']

DATA_URL = "https://raw.githubusercontent.com/owid/monkeypox/refs/heads/main/owid-monkeypox-data.csv"
df = pd.read_csv(DATA_URL)
# Filter data for the United States
afr_df = df[df['iso_code'] == 'ZAF']

#main columns
columns_of_intrest = ['location','total_cases','total_deaths','date']
afr_df=afr_df[columns_of_intrest]
spain_df= spain_df[columns_of_intrest]
#cleans the data 
spain_df = spain_df.dropna()
afr_df = afr_df.dropna()

#combines both datasets
combined_df = pd.concat([spain_df, afr_df])

#adds the combind datasets to a csv file
combined_df.to_csv("cleaned_up_data", index=False)

file =open("cleaned_up_data.csv","r")
dataIn = file.read()
myList = dataIn.split(",")
print(type(myList))

#sorting list
file =open("cleaned_up_data.csv","r")
myList = file.read()
myList.sort()
print(myList)
#list comprehention converting float into int
file =open("cleaned_up_data.csv","r")
dataIn = file.read()
myList = dataIn.split(",")
myList = [int(float(item)) for item in myList]
file.close()

