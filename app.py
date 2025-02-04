from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Prevents GUI error
import io
import base64

app = Flask(__name__)

# Load and preprocess data
DATA_URL = "https://raw.githubusercontent.com/owid/monkeypox/refs/heads/main/owid-monkeypox-data.csv"
df = pd.read_csv(DATA_URL)

# Filter data for Spain and the UK
spain_df = df[df['iso_code'] == 'ESP']
uk_df = df[df['iso_code'] == 'GBR']

# Select relevant columns
columns_of_interest = ['location', 'total_cases', 'total_deaths', 'date']
uk_df = uk_df[columns_of_interest]
spain_df = spain_df[columns_of_interest]

# Clean the data
spain_df = spain_df.dropna()
uk_df = uk_df.dropna()

# Combine datasets
combined_df = pd.concat([spain_df, uk_df])

# Convert date to Year-Month format
combined_df['date'] = pd.to_datetime(combined_df['date'])
combined_df['Year-Month'] = combined_df['date'].dt.to_period('M')

# Aggregate data by month
monthly_data = combined_df.groupby(['location', 'Year-Month']).sum().reset_index()

# Save cleaned data
monthly_data.to_csv("monthly_cleaned_data.csv", index=False)

def generate_plot():
    df = pd.read_csv("monthly_cleaned_data.csv")

    #Ensure data types are correct
    df["Year-Month"] = pd.to_datetime(df["Year-Month"].astype(str))  # Convert to datetime
    df["total_cases"] = pd.to_numeric(df["total_cases"], errors="coerce")  # Ensure numeric
    df["total_deaths"] = pd.to_numeric(df["total_deaths"], errors="coerce")  # Ensure numeric

    #Drop rows with missing values
    df = df.dropna()

    #Aggregate data so we get one total value per month instead of multiple lines
    df_grouped = df.groupby("Year-Month")[["total_cases", "total_deaths"]].sum().reset_index()

    #Extract columns for plotting
    month_data = df_grouped["Year-Month"]
    processed_case_data = df_grouped["total_cases"]
    processed_death_data = df_grouped["total_deaths"]

    #Plot the Graph
    fig, ax1 = plt.subplots(figsize=(12, 6))

    #Plot total cases (Blue)
    ax1.plot(month_data, processed_case_data, color="blue", marker="o", linestyle="-", label="Total Cases")
    ax1.set_xlabel("Time (Year-Month)")
    ax1.set_ylabel("Total Cases", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True, linestyle="--", alpha=0.5)

    #Plot total deaths (Red) on secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(month_data, processed_death_data, color="red", marker="s", linestyle="--", label="Total Deaths")
    ax2.set_ylabel("Total Deaths", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    #Improve x-axis readability
    plt.xticks(rotation=45)
    plt.title("Total Cases and Total Deaths Over Time")

    #Add lables (for both lines)
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.legend()

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url


@app.route('/')
def home():
    """Render homepage with stats and graph"""
    max_cases = monthly_data['total_cases'].max()
    min_cases = monthly_data['total_cases'].min()
    total_cases = monthly_data['total_cases'].sum()
    average_cases = round(total_cases / len(monthly_data), 2)

    max_deaths = monthly_data['total_deaths'].max()
    min_deaths = monthly_data['total_deaths'].min()
    total_deaths = monthly_data['total_deaths'].sum()
    average_deaths = round(total_deaths / len(monthly_data), 2)

    graph = generate_plot()

    return render_template('index.html', max_cases=max_cases, min_cases=min_cases, total_cases=total_cases,
                           average_cases=average_cases, max_deaths=max_deaths, min_deaths=min_deaths,
                           total_deaths=total_deaths, average_deaths=average_deaths, graph=graph)


@app.route('/api/data')
def get_data():
    """Return JSON data"""
    return jsonify({
        "max_cases": monthly_data['total_cases'].max(),
        "min_cases": monthly_data['total_cases'].min(),
        "total_cases": monthly_data['total_cases'].sum(),
        "average_cases": round(monthly_data['total_cases'].sum() / len(monthly_data), 2),
        "max_deaths": monthly_data['total_deaths'].max(),
        "min_deaths": monthly_data['total_deaths'].min(),
        "total_deaths": monthly_data['total_deaths'].sum(),
        "average_deaths": round(monthly_data['total_deaths'].sum() / len(monthly_data), 2),
    })



if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0", port=8000)  # Change port number
