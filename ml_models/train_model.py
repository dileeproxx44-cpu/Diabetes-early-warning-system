import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from preprocess import preprocess_data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load processed data
X_train, X_test, y_train, y_test = preprocess_data()

# =====================================
# RANDOM FOREST MODEL
# =====================================

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_predictions)

print(f"Random Forest Accuracy: {rf_accuracy * 100:.2f}%")

# Save model
rf_model_path = os.path.join(
    BASE_DIR,
    'random_forest_model.pkl'
)

joblib.dump(rf_model, rf_model_path)

# =====================================
# LOGISTIC REGRESSION MODEL
# =====================================

lr_model = LogisticRegression()

lr_model.fit(X_train, y_train)

lr_predictions = lr_model.predict(X_test)

lr_accuracy = accuracy_score(y_test, lr_predictions)

print(f"Logistic Regression Accuracy: {lr_accuracy * 100:.2f}%")

# Save model
lr_model_path = os.path.join(
    BASE_DIR,
    'logistic_model.pkl'
)

joblib.dump(lr_model, lr_model_path)

# =====================================
# SVM MODEL
# =====================================

svm_model = SVC(
    probability=True
)

svm_model.fit(X_train, y_train)

svm_predictions = svm_model.predict(X_test)

svm_accuracy = accuracy_score(y_test, svm_predictions)

print(f"SVM Accuracy: {svm_accuracy * 100:.2f}%")

# Save model
svm_model_path = os.path.join(
    BASE_DIR,
    'svm_model.pkl'
)

joblib.dump(svm_model, svm_model_path)

# =====================================
# DECISION TREE MODEL
# =====================================

dt_model = DecisionTreeClassifier(
    random_state=42
)

dt_model.fit(X_train, y_train)

dt_predictions = dt_model.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_predictions)

print(f"Decision Tree Accuracy: {dt_accuracy * 100:.2f}%")

# Save model
dt_model_path = os.path.join(
    BASE_DIR,
    'decision_tree_model.pkl'
)

joblib.dump(dt_model, dt_model_path)

# =====================================
# FINAL MESSAGE
# =====================================

print("All models saved successfully.")