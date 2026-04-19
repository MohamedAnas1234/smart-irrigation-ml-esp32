import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 🔹 Load dataset
df = pd.read_csv("soil_dataset_600_rows.csv")

# 🔹 Use ONLY soil (IMPORTANT FIX)
X = df[["soil"]]
y = df["label"]

# 🔹 Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 🔹 Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# 🔹 Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 Accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# 🔹 Manual test (CRITICAL)
print("\nManual Test:")
test_values = [1200, 2000, 3500, 4095]

for val in test_values:
    sample = pd.DataFrame([[val]], columns=["soil"])
    pred = model.predict(sample)
    print(f"Soil={val} → {le.inverse_transform(pred)[0]}")

# 🔹 Save model
joblib.dump(model, "model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("\nModel saved successfully!")