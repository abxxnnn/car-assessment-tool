import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import classification_report
import joblib

# Load the dataset
df = pd.read_csv("car_inspection_dataset_balanced.csv")
X = df.iloc[:, :155]
y = df["Rating"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Parameter grid for RandomizedSearchCV
param_grid = {
    "n_estimators": [50, 100, 200, 300],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "max_features": ["sqrt", "log2", None]
}

# Random forest
rf = RandomForestClassifier(random_state=42)

# Randomized Search
search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_grid,
    n_iter=20,              # Try 20 combinations
    cv=3,                   # 3-fold cross-validation
    n_jobs=-1,
    verbose=2,
    random_state=42
)

search.fit(X_train, y_train)

# Best model
best_model = search.best_estimator_

# Evaluate
y_pred = best_model.predict(X_test)
print("🔍 Best Parameters:", search.best_params_)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save
joblib.dump(best_model, "car_rating_model_tuned.pkl")
print("\n✅ Tuned model saved as car_rating_model_tuned.pkl")
