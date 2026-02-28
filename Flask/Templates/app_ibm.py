from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("payments.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict_page")
def predict_page():
    return render_template("predict.html")

@app.route("/predict", methods=["POST"])
def predict():
    type_ = float(request.form["type"])
    amount = float(request.form["amount"])
    oldbalanceOrg = float(request.form["oldbalanceOrg"])
    newbalanceOrig = float(request.form["newbalanceOrig"])
    oldbalanceDest = float(request.form["oldbalanceDest"])
    newbalanceDest = float(request.form["newbalanceDest"])

    input_data = np.array([[type_, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]])
    pred = model.predict(input_data)

    if pred[0] == 1:
        output = "⚠ Fraud Transaction Detected!"
    else:
        output = "✅ Safe Transaction"

    return render_template("submit.html", prediction=output)

if __name__ == "__main__":
    app.run(debug=True)