from flask import Flask, render_template, request
from diet_utils import generate_diet_plan

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    age = int(request.form["age"])
    gender = request.form["gender"]
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    activity = request.form["activity"]
    goal = request.form["goal"]

    plan = generate_diet_plan(
        age=age,
        gender=gender,
        height=height,
        weight=weight,
        activity=activity,
        goal=goal
    )

    return render_template(
        "result.html",
        plan=plan
    )


if __name__ == "__main__":
    app.run(debug=True)