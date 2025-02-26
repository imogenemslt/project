from flask import Flask, render_template, request, redirect, jsonify
import csv
import json
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)

# Function to read steps.csv data
def get_data():
    try:
        with open("monthly_cleaned_data.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) < 2:  # If only header exists or empty file
            return []
        
        data.pop(0)  # Remove header
        return data
    except FileNotFoundError:
        return []

# Function to create a Plotly graph
def make_graph(monkeypox_data):
    if not monkeypox_data:  # Handle missing data gracefully
        return json.dumps({})

    try:
        dates = [row[4] for row in monkeypox_data]
        cases = [int(row[1]) for row in monkeypox_data]
    except (IndexError, ValueError):  # Handle data errors
        return json.dumps({})

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=date, y=cases, mode='lines+markers',
        marker=dict(color='red'),
        name="monkeypox data"
    ))

    fig.update_layout(
        title="Interactive Graph for cases",
        xaxis_title="date",
        yaxis_title="cases",
        xaxis=dict(tickangle=45),
        template="plotly_white"  # Optional: Change theme
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Home route
@app.route("/")
def homepage():
    return render_template("index.html")

# View data route
@app.route("/viewData")
def view_data():
    data = get_data()
    graphJSON = make_graph(data)  # Generate graph JSON
    return render_template("viewData.html", info=data, graphJSON=graphJSON)

# Add data route
@app.route("/addData", methods=["GET", "POST"])
def add_data():
    if request.method == "POST":
        date = request.form.get("date")
        cases = request.form.get("cases")
        with open("monthly_cleaned_data.csv", "a") as file:
            file.write(f"{date},{steps}\n")
        return redirect("/viewData")
    return render_template("addData.html")






if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
