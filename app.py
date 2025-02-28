from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("phishing_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        url_length = int(request.form["url_length"])
        https_token = int(request.form["https_token"])
        having_at_symbol = int(request.form["having_at_symbol"])
        
        # Create a dataframe for prediction
        features = pd.DataFrame([[url_length, https_token, having_at_symbol]],
                                columns=["URL_Length", "HTTPS_token", "having_At_Symbol"])
        
        # Predict using the model
        prediction = model.predict(features)[0]
        result = "Phishing" if prediction == 1 else "Legitimate"
        
        return render_template("index.html", result=result)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
