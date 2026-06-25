import streamlit as st
import pandas as pd
import requests
from datetime import datetime

API = "http://127.0.0.1:8000"

session = requests.Session()
session.trust_env = False

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="NYC Taxi Fare Prediction",
    page_icon="🚖",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
}

/* ---- Hero Header ---- */
.hero-title {
    font-size: 42px;
    font-weight: bold;
    color: white;
    margin-bottom: 6px;
}

.hero-subtitle {
    color: #AAAAAA;
    font-size: 17px;
}

/* ---- Cards ---- */
.card {
    background-color: #1E1E1E;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #333;
}

.metric-card {
    background-color: #1A1F2E;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-top: 15px;
}

.metric-value {
    font-size: 35px;
    font-weight: bold;
    color: #FFD43B;
}

.metric-title {
    color: white;
    font-size: 18px;
}

/* ---- Predict Button ---- */
.stButton > button {
    width: 100%;
    background-color: #FFD43B;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 50px;
    border: none;
}

/* ---- Passenger icon buttons ---- */
div[data-testid="column"] .stButton > button {
    width: 100%;
    height: 60px;
    font-size: 20px;
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #444;
    border-radius: 10px;
    transition: all 0.2s;
}

div[data-testid="column"] .stButton > button:hover {
    border-color: #FFD43B;
    color: #FFD43B;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "passenger_count" not in st.session_state:
    st.session_state.passenger_count = 1

if "result" not in st.session_state:
    st.session_state.result = None

# =========================
# HERO HEADER  (title جنب الصورة)
# =========================

hero_text_col, hero_img_col = st.columns([2, 1])

with hero_text_col:
    st.markdown("<div class='hero-title'>🚖 NYC Taxi Fare Prediction</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Predict taxi fares using Machine Learning & XGBoost</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

with hero_img_col:
    # غير المسار ده لمسار الصورة عندك
    st.image(
        r"D:\Uni_Bedo\Projects_Bedo\ML_project\Uber-Fare-Prediction\taxi-and-bus-photo.jpg",
        use_container_width=True
    )

st.divider()

# =========================
# LAYOUT  (inputs | result)
# =========================

col1, col2 = st.columns([1, 1])

# =========================
# INPUT SECTION
# =========================

with col1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📍 Ride Details")

    pickup_longitude = st.number_input("Pickup Longitude",  value=-73.99)
    pickup_latitude  = st.number_input("Pickup Latitude",   value=40.75)
    dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.98)
    dropoff_latitude  = st.number_input("Dropoff Latitude",  value=40.76)

    # ---- Passenger picker بأيقونات ----
    st.markdown("**🧍 Passenger Count**")

    pax_icons = ["1 👤", "2 👥", "3 👥", "4 👥", "5 👥", "6 👥"]
    pax_cols  = st.columns(6)

    for i, col in enumerate(pax_cols):
        n = i + 1
        label = pax_icons[i]
        # نبرز الزر المختار بلون مختلف
        if st.session_state.passenger_count == n:
            col.markdown(
                f"<div style='text-align:center;background:#FFD43B;color:black;"
                f"border-radius:10px;padding:10px 0;font-size:20px;font-weight:bold'>"
                f"{label}</div>",
                unsafe_allow_html=True
            )
        else:
            if col.button(label, key=f"pax_{n}"):
                st.session_state.passenger_count = n
                st.rerun()

    passenger_count = st.session_state.passenger_count
    st.caption(f"Selected: {passenger_count} passenger{'s' if passenger_count > 1 else ''}")

    st.markdown("<br>", unsafe_allow_html=True)

    date = st.date_input("Pickup Date")
    time = st.time_input("Pickup Time")

    pickup_datetime = datetime.combine(date, time).isoformat()

    predict = st.button("🚕 Predict Fare")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PREDICTION CALL
# =========================

if predict:

    payload = {
        "pickup_longitude":  pickup_longitude,
        "pickup_latitude":   pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude":  dropoff_latitude,
        "passenger_count":   passenger_count,
        "pickup_datetime":   pickup_datetime
    }

    try:
        response = session.post(f"{API}/predict", json=payload)
        st.session_state.result = response.json()
    except Exception:
        st.error("❌ FastAPI server is not running.")
        st.session_state.result = None

# =========================
# RESULT SECTION
# =========================

with col2:

    st.subheader("💰 Prediction Result")

    result = st.session_state.result

    if result:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Predicted Fare</div>
                <div class="metric-value">${result['predicted_fare']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Trip Distance</div>
                <div class="metric-value">{result['distance_km']} km</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("Enter trip information and click Predict Fare.")

# =========================
# HISTORY
# =========================

st.divider()

st.subheader("📋 Prediction History")

try:

    rows = session.get(f"{API}/history").json()

    if rows:
        history_df = pd.DataFrame(rows)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No predictions yet.")

except Exception:
    st.warning("⚠️ FastAPI server is not running.")

# =========================
# FOOTER
# =========================

st.divider()

st.markdown(
    """
    <center>
        🚖 NYC Taxi Fare Prediction System <br>
        Powered by FastAPI + Streamlit + XGBoost <br><br>
        Developed by Abdullah
    </center>
    """,
    unsafe_allow_html=True
)