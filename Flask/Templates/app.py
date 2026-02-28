from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model = pickle.load(open("payments.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict_page")
def predict_page():
    return render_template("predict.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        type_ = float(request.form["type"])
        amount = float(request.form["amount"])
        oldbalanceOrg = float(request.form["oldbalanceOrg"])
        newbalanceOrig = float(request.form["newbalanceOrig"])
        oldbalanceDest = float(request.form["oldbalanceDest"])
        newbalanceDest = float(request.form["newbalanceDest"])

        features = np.array([[type_, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]])
        prediction = model.predict(features)

        if prediction[0] == 1:
            result = "⚠ Fraud Transaction Detected!"
        else:
            result = "✅ Safe Transaction (Not Fraud)"

        return render_template("submit.html", prediction=result)

    except Exception as e:
        return render_template("submit.html", prediction="Error: " + str(e))

if __name__ == "__main__":
    app.run(debug=True)