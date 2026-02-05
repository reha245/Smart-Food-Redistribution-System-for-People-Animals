from flask import Flask, request, render_template
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from predict import process_donation

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", result=None, dashboard=None)

@app.route("/submit", methods=["POST"])
def submit():
    names = request.form.getlist("food_name")
    types = request.form.getlist("food_type")
    quantities = request.form.getlist("quantity")
    prepared_dates = request.form.getlist("prepared_date")
    cities = request.form.getlist("city")

    food_items = []
    for i in range(len(names)):
        food_items.append({
            "food_name": names[i],
            "food_type": types[i],
            "quantity": quantities[i],
            "prepared_date": prepared_dates[i],
            "city": cities[i]
        })

    ai_result = process_donation(food_items)
    return render_template("index.html", result=ai_result["donations"], dashboard=ai_result["dashboard"])

if __name__ == "__main__":
    app.run(debug=True)