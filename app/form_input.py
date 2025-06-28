
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from utils import score_to_rating

st.set_page_config(page_title="Used Car Inspection Form", layout="wide")
st.title("🚗 Used Car Inspection Form")

parameter_groups = {
    "1. Vehicle Identification & History": {
        "VIN matches registration/documents": 10,
        "Clean title (not salvaged or rebuilt)": 10,
        "Service records available and complete": 7,
        "Number of previous owners": 5,
        "Accident history (via Carfax/inspection)": 10,
        "Insurance claims history": 7,
        "Odometer tampering signs": 10,
        "Recalls and service bulletins checked": 5,
        "Pollution certificate valid": 7,
        "Loan or financial lien clearance": 10
    },
    "2. Exterior Inspection": {
        "Paint uniformity & overspray signs": 5,
        "Scratches, dents, or rust spots": 5,
        "Frame damage or weld marks": 10,
        "Door/fender alignment & gaps": 7,
        "Windshield cracks or chips": 10,
        "Headlights & taillights lens condition": 5,
        "Wiper blades condition": 2,
        "Side mirror stability and cracks": 5,
        "Door operation (hinges, locks, handles)": 5,
        "Trunk operation and seal": 5,
        "Sunroof/moonroof functionality": 5,
        "Hood alignment and latch": 5,
        "Mud flaps and underbody protection": 2,
        "Number plate condition and visibility": 2,
        "Condition of emblems and trims": 2,
        "Body rust check (sill, wheel well)": 10,
        "Window glass scratches/tint legality": 5,
        "Roof condition and dent checks": 5,
        "Fender inner linings": 5,
        "Undercarriage corrosion/leaks": 10
    },
    "3. Engine & Powertrain": {
        "Cold start performance": 10,
        "Engine noise (tapping, knocking)": 10,
        "Engine bay cleanliness and oil leaks": 10,
        "Fluid levels (engine oil, coolant, brake)": 10,
        "Fluid condition (color/smell)": 10,
        "Engine mount condition": 7,
        "Timing belt/chain service done": 10,
        "Air filter condition": 5,
        "Battery health (age, terminals, voltage)": 7,
        "Alternator charging output": 7,
        "Starter motor function": 7,
        "Fuel injector or pump noise": 7,
        "Engine check light or codes": 10,
        "Smoke from exhaust (color test)": 10,
        "Idling RPM stability": 10,
        "Engine overheating signs": 10,
        "Radiator fan operation": 10,
        "Radiator leaks or rust": 10,
        "Engine oil level and color": 10,
        "Coolant color and level": 10,
        "Fuel line condition": 10,
        "Crankshaft and belts condition": 7,
        "Drive belts – noise/wear": 7,
        "Engine cover secure": 2,
        "Dipstick and cap seal": 7
    },
    "4. Transmission & Clutch": {
        "Smooth gear shifts (auto/manual)": 10,
        "Clutch bite point and travel": 7,
        "Clutch slipping signs": 10,
        "Transmission oil level & color": 7,
        "Gearstick movement & noise": 7,
        "Creaks or hesitation during gear change": 10,
        "Automatic gearbox responsiveness": 10,
        "Transmission warning lights": 10,
        "Reverse gear function": 10,
        "Clutch pedal play/return": 7,
        "Clutch fluid level (if hydraulic)": 7,
        "Gear sync issues (grinding/hard shift)": 10,
        "Dual clutch/AMT test if applicable": 10,
        "Transmission mount check": 7,
        "Paddle shifter operation (if present)": 5
    },
    "5. Suspension, Tyres & Steering": {
        "Uneven tyre wear": 10,
        "Tyre age & tread depth (all 5 tyres)": 10,
        "Suspension noise on bumps": 10,
        "Shock absorber leaks": 10,
        "Steering response/play": 10,
        "Alignment and straight drive test": 10,
        "Steering noise while turning": 10,
        "Ball joints and tie rods": 10,
        "Power steering fluid level": 7,
        "Suspension bush wear": 7,
        "Axle/CV joint noise": 10,
        "Steering return after turn": 7,
        "Tyre brand consistency": 5,
        "Spare tyre & jack presence": 5,
        "Rim dents or cracks": 7,
        "Wheel nuts/bolts tightness": 5,
        "Underbody suspension rust": 10,
        "Ride height consistency": 5,
        "Wheel bearing noise": 10,
        "Tyre pressure status": 5
    },
    "6. Braking System": {
        "Brake pad thickness": 10,
        "Brake disc/rotor condition": 10,
        "Brake fluid level & color": 10,
        "ABS warning light check": 10,
        "Emergency brake/handbrake function": 10,
        "Spongy or hard brake pedal": 10,
        "Brake pulling (left/right)": 10,
        "Brake lines leak or rust": 10,
        "Brake booster check": 10,
        "Noise during braking": 10
    },
    "7. Electricals & Lighting": {
        "Headlights (high/low beam)": 5,
        "Indicator & hazard lights": 5,
        "Fog lamps (front/rear)": 5,
        "Cabin lights and map lights": 2,
        "Brake lights": 10,
        "Reverse lights": 10,
        "Horn functionality": 10,
        "Power window operation": 5,
        "Central locking & remote key": 5,
        "Key fob battery or push start": 5,
        "Infotainment/audio system": 5,
        "Bluetooth/USB/AUX": 5,
        "Steering-mounted controls": 5,
        "Digital console & display": 5,
        "Speedometer & odometer": 10,
        "Warning lights (battery, oil, ABS)": 10,
        "AC/Heater blower": 5,
        "Power mirror adjustment": 5,
        "Rear defogger": 5,
        "Sunshade, wiper motor, washer jets": 5
    },
    "8. Interior Cabin & Features": {
        "Seat upholstery condition": 5,
        "Seat adjustment (manual/electric)": 5,
        "Seat belt operation & lock": 10,
        "Dashboard cracks or rattles": 5,
        "Carpet and floor mats": 2,
        "Roof liner condition": 5,
        "Glove box and compartments": 2,
        "AC cooling and vent operation": 5,
        "Cabin odor (mold/pets/smoke)": 5,
        "Window seals for air/noise leaks": 5,
        "Interior plastics and trims": 5,
        "Center console functionality": 5,
        "Sun visor operation": 2,
        "Rear seat condition & space": 5,
        "Child lock & ISOFIX mounts": 10,
        "Door trim and handle quality": 5,
        "Seat height adjustment": 5,
        "Cup holders, charging ports": 5,
        "Cabin noise on drive": 5,
        "Dashboard panel fitting": 5
    },
    "9. Test Drive Evaluation": {
        "Cold start & idle observation": 10,
        "Acceleration response": 10,
        "Engine vibration and noise": 10,
        "Gear shift during drive": 10,
        "Clutch feel and return": 10,
        "Steering feedback and return": 10,
        "Suspension feel over potholes": 10,
        "Brake responsiveness": 10,
        "HVAC performance while driving": 5,
        "Cabin rattles/squeaks": 5,
        "Wind noise at high speed": 5,
        "Drive straight without pulling": 10,
        "Parking test (tight turns)": 7,
        "Reverse and hill-hold test": 10,
        "Overall comfort and confidence": 5
    }
}

# Load saved draft if exists
draft_file = Path("data/form_draft.json")
if draft_file.exists():
    with open(draft_file, "r") as f:
        saved_data = json.load(f)
else:
    saved_data = {}

# Store raw slider values
raw_slider_values = {}
for section, items in parameter_groups.items():
    with st.expander(section, expanded=False):
        for param, weight in items.items():
            default_val = saved_data.get(param, 0)
            raw_val = st.slider(param, 0, 5, int(default_val), step=1)
            raw_slider_values[param] = raw_val

# Auto-save raw values
with open(draft_file, "w") as f:
    json.dump(raw_slider_values, f)

# Setup session state
if "stage" not in st.session_state:
    st.session_state.stage = "start"
if "result" not in st.session_state:
    st.session_state.result = None

# ────────────────────────────────────────────────
# ✅ Score calculation logic (now correct)
# ────────────────────────────────────────────────
def calc_score():
    total = sum(raw_slider_values[param] * weight for section in parameter_groups.values() for param, weight in section.items())
    max_score = sum(weight * 5 for section in parameter_groups.values() for weight in section.values())
    normalized = round((total / max_score) * 10, 1)
    return total, max_score, normalized

def go_to_confirm():
    st.session_state.stage = "confirm"

def finalize_submission():
    total, max_score, rating10 = calc_score()
    st.session_state.result = (total, max_score, rating10)
    st.session_state.final_scores = {
        param: raw_slider_values[param] * weight
        for section in parameter_groups.values()
        for param, weight in section.items()
    }
    st.session_state.stage = "finalized"
    if draft_file.exists():
        draft_file.unlink()


def cancel_submission():
    st.session_state.stage = "start"

# ────────────────────────────────────────────────
# UI State Logic
# ────────────────────────────────────────────────

if st.session_state.stage == "start":
    st.button("✅ Submit Inspection", key="submit_btn", on_click=go_to_confirm)

elif st.session_state.stage == "confirm":
    st.warning("⚠️ Please confirm you want to submit this inspection.")
    c1, c2 = st.columns(2)
    with c1:
        st.button("✅ Confirm Submission", key="confirm_btn", on_click=finalize_submission)
    with c2:
        st.button("❌ Cancel Submission", key="cancel_btn", on_click=cancel_submission)

elif st.session_state.stage == "finalized" and st.session_state.result:
    total, max_score, rating10 = st.session_state.result
    st.success(f"🎯 Final Score: {rating10} / 10")
    st.info(f"🚦 Rating: {score_to_rating(rating10)}")

    # Rating Guide
    st.markdown("""
    <div style="background:#111;padding:16px;border-radius:6px;color:#eee;font-size:15px;">
      <b>📊 Rating Guide:</b><br><br>
      Each parameter is rated from <b>0 to 5</b> and multiplied by its weight. Final score is normalized to 10.<br><br>
      <span style="color:#00bfff">8.6 – 10.0</span>: 🌟 Excellent (Almost like new)<br>
      <span style="color:#00cc66">7.3 – 8.5</span>: ✅ Very Good<br>
      <span style="color:#ffcc00">5.9 – 7.2</span>: 🟡 Good (Minor repairs needed)<br>
      <span style="color:#ffa500">4.5 – 5.8</span>: ⚠️ Average (Significant repairs needed)<br>
      <span style="color:#ff4d4d">Below 4.5</span>: ❌ Avoid unless very cheap
    </div>
    """, unsafe_allow_html=True)

import io

# Export Options
st.write("### 💾 Export Options")
col1, col2 = st.columns(2)

# Calculate full weighted scores again
final_scores = st.session_state.get("final_scores", {})

# Convert to DataFrame
df = pd.DataFrame([final_scores])
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

with col1:
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📁 Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"inspection_{ts}.csv",
        mime="text/csv"
    )

with col2:
    json_data = json.dumps(final_scores, indent=2)
    st.download_button(
        label="📦 Download JSON",
        data=json_data,
        file_name=f"inspection_{ts}.json",
        mime="application/json"
    )
