import streamlit as st
import pandas as pd
import joblib
from utils import score_to_rating

# Load models
clf_model = joblib.load("models/car_rating_model_tuned.pkl")
reg_model = joblib.load("models/car_score_model.pkl")

st.set_page_config(page_title="Used Car Evaluator", layout="wide")
st.title("🚗 Used Car Inspection Evaluator")

st.write("Upload a 155-point checklist (CSV file). We'll predict the car's **total score** and its **rating**.")

uploaded_file = st.file_uploader("📤 Upload CSV file (1 row = 1 car)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if df.shape[1] != 155:
            st.error("❌ CSV must have exactly 155 columns (one for each checklist item).")
        else:
            st.success("✅ File uploaded successfully!")

            # Predict score
            score_pred = reg_model.predict(df)[0]
            rating_pred = score_to_rating(score_pred)

            # Predict rating (from classifier model)
            clf_pred = clf_model.predict(df)[0]

            st.markdown("### 🔍 Results")
            st.metric("Predicted Score", f"{score_pred:.1f} / 1100")
            st.metric("Final Rating", f"{rating_pred}")
            st.metric("Classifier Suggests", f"{clf_pred}")

            st.markdown("💡 *Score-based rating is preferred as it gives continuous feedback.*")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
