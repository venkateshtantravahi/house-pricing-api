import pandas as pd
import joblib
from flask import Flask, request, jsonify
import sklearn
import os
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# --- 1. Load the Champion Model ---
# We load the model globally so it stays in memory.
# Loading it inside the function would be too slow for high-traffic apps.
print("Loading model pipeline...")
try:
    model = joblib.load('model/housing_model.joblib')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file not found.")


@app.route('/')
def home():
    """Health check route to ensure the app is running."""
    return jsonify({"status": "online",
                    "message": "House Price Prediction API is active."})


@app.route('/predict', methods=['POST'])
def predict():
    """
    Accepts JSON data, creates a DataFrame, and returns a price prediction.
    """
    try:
        # --- 2. Receive & Parse Data ---
        data = request.get_json()

        # We extract the specific features our model expects.
        # This acts as a filter, ignoring any extra junk data sent by the user.
        input_data = {
            'MedInc': data['MedInc'],  # Median Income
            'HouseAge': data['HouseAge'],  # Age of the house
            'AveRooms': data['AveRooms'],  # Avg rooms per household
            'AveBedrms': data['AveBedrms'],  # Avg bedrooms
            'Population': data['Population'],  # Block population
            'AveOccup': data['AveOccup']
        }

        # Convert to DataFrame (Scikit-Learn expects this format)
        input_df = pd.DataFrame([input_data])

        # --- 3. Generate Prediction ---
        prediction = model.predict(input_df)

        # Calculate the actual dollar value (target was scaled in $100k units)
        price_in_100k = prediction[0]
        price_in_usd = price_in_100k * 100000

        # Return the result in a clean JSON format
        return jsonify({
            "status": "success",
            "input_features": input_data,
            "prediction": {
                "price_100k_units": float(price_in_100k),
                "estimated_value_usd": round(float(price_in_usd), 2)
            }
        })

    except KeyError as e:
        # Handle missing fields (e.g., user forgot 'MedInc')
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        # Handle other unforeseen errors
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run the server locally on port 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)