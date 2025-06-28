import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("car_inspection_dataset_balanced.csv")

# If "Score" column is missing, compute it
if "Score" not in df.columns:
    df["Score"] = df.iloc[:, :155].sum(axis=1)

# Features and target
X = df.iloc[:, :155]
y = df["Score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("📏 MAE:", round(mae, 2))
print("📈 R² Score:", round(r2, 3))

# Save model
joblib.dump(model, "car_score_model.pkl")
print("✅ Score prediction model saved as car_score_model.pkl")
