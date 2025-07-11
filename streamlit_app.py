import streamlit as st
import requests

# ✅ Set custom page title & icon
st.set_page_config(
    page_title="FlowGuard Predictor",
    page_icon="🛡️",
    layout="centered",
)

# ✅ API URL
API_URL = "https://flowguard-api-938724554929.europe-west1.run.app/predict"

# ✅ App Title & Intro
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #4B6EF5;">🛡️ FlowGuard</h1>
        <p style="font-size: 18px;">Predict whether a network connection is <b>benign</b> or <b>malicious</b> in real time.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ Add logo (optional)
# st.image("https://YOUR_LOGO_URL", width=120)

st.markdown("---")

# ✅ Input Form
st.header("🔢 Connection Details")

col1, col2 = st.columns(2)

with col1:
    proto = st.text_input("Protocol")
    conn_state = st.text_input("Connection State")
    history = st.text_input("History")

with col2:
    duration = st.number_input("Duration (seconds)")
    orig_pkts = st.number_input("Originator Packets")
    orig_ip_bytes = st.number_input("Originator IP Bytes")

st.markdown("---")

# ✅ Predict Button
if st.button("🔍 Predict"):
    input_data = {
        "proto": proto,
        "conn_state": conn_state,
        "history": history,
        "duration": duration,
        "orig_pkts": orig_pkts,
        "orig_ip_bytes": orig_ip_bytes
    }

    with st.spinner("🔄 Sending data to FlowGuard API..."):
        try:
            response = requests.post(API_URL, json=input_data)
            if response.status_code == 200:
                prediction = response.json()["prediction"]

                st.markdown("### 🧩 Result")
                if prediction == "benign connection":
                    st.success(f"✅ **Prediction:** {prediction}")
                else:
                    st.error(f"🚨 **Prediction:** {prediction}")

            else:
                st.error(f"❌ API Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")

st.markdown(
    """
    <hr style="border-top: 1px solid #bbb;">
    <p style="text-align: center; font-size: 14px; color: #888;">© 2025 FlowGuard Cybersecurity</p>
    """,
    unsafe_allow_html=True
)
