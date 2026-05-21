import os
import joblib
import numpy as np


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# ==============================
# LOAD MODEL
# ==============================

model_path = os.path.join(
    BASE_DIR,
    'random_forest_model.pkl'
)

scaler_path = os.path.join(
    BASE_DIR,
    'scaler.pkl'
)

model = joblib.load(model_path)

scaler = joblib.load(scaler_path)


# ==============================
# PREDICTION FUNCTION
# ==============================

def predict_disease(data):

    data = np.array(data).reshape(1, -1)

    scaled_data = scaler.transform(data)

    prediction = model.predict(scaled_data)[0]

    probability = model.predict_proba(
        scaled_data
    )[0][1] * 100

    if prediction == 1:

        result = "High Risk of Diabetes"

    else:

        result = "Low Risk of Diabetes"

    return result, round(probability, 2)