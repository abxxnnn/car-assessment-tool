import pandas as pd
import joblib
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("car_inspection_dataset_balanced.csv")
X = df.iloc[:, :155]
y = df["Rating"]

# Load tuned model
model = joblib.load("car_rating_model_tuned.pkl")

# Step 2️⃣: 5-Fold Cross-Validation
cv_scores = cross_val_score(model, X, y, cv=5)
print("🔁 5-Fold Cross-Validation Accuracy Scores:", cv_scores)
print("✅ Mean Accuracy: {:.2f}%".format(cv_scores.mean() * 100))

# Step 3️⃣: Feature Importance Plot
importances = model.feature_importances_
indices = importances.argsort()[::-1]
top_n = 20  # Top 20 features

plt.figure(figsize=(10, 6))
sns.barplot(x=importances[indices[:top_n]], y=[f"Item_{i+1}" for i in indices[:top_n]])
plt.title("Top 20 Important Checklist Items")
plt.xlabel("Importance Score")
plt.ylabel("Checklist Feature")
plt.tight_layout()
plt.show()
