import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def preprocess_data():

    dataset_path = os.path.join(
        BASE_DIR,
        '..',
        'datasets',
        'diabetes.csv'
    )

    df = pd.read_csv(dataset_path)

    # Encode gender
    df['gender'] = df['gender'].replace({
        'Male': 1,
        'Female': 0,
        'Other': 2
    })

    # Encode smoking history
    smoking_map = {
        'never': 0,
        'No Info': 1,
        'current': 2,
        'former': 3,
        'ever': 4,
        'not current': 5
    }

    df['smoking_history'] = df['smoking_history'].map(smoking_map)

    # Features and target
    X = df.drop('diabetes', axis=1)

    y = df['diabetes']

    # Scaling
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Save scaler
    scaler_path = os.path.join(
        BASE_DIR,
        'scaler.pkl'
    )

    joblib.dump(scaler, scaler_path)

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test