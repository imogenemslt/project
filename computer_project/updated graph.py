import csv
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV into a Pandas DataFrame
df = pd.read_csv("monthly_cleaned_data.csv")

# Ensure data types are correct
df["Year-Month"] = pd.to_datetime(df["Year-Month"].astype(str))  # Convert to datetime
df["total_cases"] = pd.to_numeric(df["total_cases"], errors="coerce")  # Ensure numeric
df["total_deaths"] = pd.to_numeric(df["total_deaths"], errors="coerce")  # Ensure numeric

# Drop rows with missing values
df = df.dropna()

# 🔥 Aggregate data so we get **one total value per month** instead of multiple lines
df_grouped = df.groupby("Year-Month")[["total_cases", "total_deaths"]].sum().reset_index()

# Extract columns for plotting
month_data = df_grouped["Year-Month"]
processed_case_data = df_grouped["total_cases"]
processed_death_data = df_grouped["total_deaths"]

# --- Plot the Graph ---
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot total cases (Blue)
ax1.plot(month_data, processed_case_data, color="blue", marker="o", linestyle="-", label="Total Cases")
ax1.set_xlabel("Time (Year-Month)")
ax1.set_ylabel("Total Cases", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.grid(True, linestyle="--", alpha=0.5)

# Plot total deaths (Red) on secondary y-axis
ax2 = ax1.twinx()
ax2.plot(month_data, processed_death_data, color="red", marker="s", linestyle="--", label="Total Deaths")
ax2.set_ylabel("Total Deaths", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Improve x-axis readability
plt.xticks(rotation=45)
plt.title("Total Cases and Total Deaths Over Time")

# Add legend (for both lines)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

# Show the plot
plt.tight_layout()
plt.show()
