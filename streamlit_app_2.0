import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

API_URL = "https://flowguard-api-938724554929.europe-west1.run.app/batch_predict"

st.set_page_config(page_title="FlowGuard Batch Predictor", page_icon="🛡️")

st.title("🛡️ FlowGuard - Batch Network Predictor")
st.markdown("Upload a CSV file with connection metadata and get a full prediction report.")

st.markdown("---")

uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Uploaded File")
    st.write(df.head())

    required_cols = ["proto", "conn_state", "history", "duration", "orig_pkts", "orig_ip_bytes"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
    else:
        clean_df = df[required_cols]

        if st.button("🚀 Run Batch Prediction"):
            with st.spinner("Processing..."):
                # ✅ Send entire DataFrame for batch prediction
                input_data = clean_df.to_dict(orient="records")
                response = requests.post(API_URL, json={"instances": input_data})

                if response.status_code == 200:
                    predictions = response.json()["predictions"]
                    clean_df["prediction"] = predictions

                    st.success("✅ Batch prediction complete!")

                    # ✅ Dashboard
                    total = len(clean_df)
                    benign = (clean_df["prediction"] == "benign connection").sum()
                    malicious = (clean_df["prediction"] == "malicious connection").sum()

                    st.write(f"**Total:** {total}")
                    st.write(f"✅ Benign: {benign}")
                    st.write(f"🚨 Malicious: {malicious}")

                    st.progress(benign / total)

                    st.bar_chart(pd.DataFrame({
                        "Label": ["Benign", "Malicious"],
                        "Count": [benign, malicious]
                    }).set_index("Label"))

                    st.subheader("🚨 Malicious Connections")
                    st.write(clean_df[clean_df["prediction"] == "malicious connection"])

                    # ✅ Download results
                    st.download_button(
                        label="📥 Download Results",
                        data=clean_df.to_csv(index=False).encode(),
                        file_name="flowguard_batch_results.csv",
                        mime="text/csv",
                    )

                    # ✅ Append to log file
                    log_df = clean_df.copy()
                    log_df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("prediction_log.csv", "a") as f:
                        log_df.to_csv(f, index=False, header=f.tell() == 0)

                else:
                    st.error(f"❌ API Error: {response.text}")
