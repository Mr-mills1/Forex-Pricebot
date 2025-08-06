
from flask import Flask, request, render_template
import numpy as np
import os
import pickle

app = Flask(__name__)

# List of available models (currency codes)
currency_codes = [
    'audjpy', 'audcad', 'eurusd', 'gbpusd', 'usdjpy', 'gbpjpy', 
    'audusd', 'nzdusd', 'eurgbp', 'euraud'
]

models = {}
for code in currency_codes:
    model_path = f"models/{code.upper()}_xgb.pkl"
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            models[code] = pickle.load(f)


# Rendered template for GET/POST
@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    selected_currency = None
    error = None
    if request.method == "POST":
        selected_currency = request.form.get("currency", "").lower()
        try:
            open_ = float(request.form.get("open"))
            high = float(request.form.get("high"))
            low = float(request.form.get("low"))
            sma5 = float(request.form.get("sma5"))
            if selected_currency not in models:
                error = "Model not found for this currency."
            else:
                model = models[selected_currency]
                X = np.array([[open_, high, low, sma5]])
                pred = model.predict(X)
                prediction = round(float(pred[0]), 4)
        except Exception as e:
            error = "Invalid input. Please enter valid numbers."
    return render_template(
        "index.html",
        currencies=currency_codes,
        selected_currency=selected_currency,
        prediction=prediction,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
