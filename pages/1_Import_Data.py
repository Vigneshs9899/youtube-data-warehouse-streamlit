import streamlit as st
import pandas as pd
from pipeline import run_pipeline

st.set_page_config(page_title="Import YouTube Data", layout="centered")

st.title("📥 Import YouTube Data")

# -----------------------------
# CHANNEL INPUT
# -----------------------------
st.header("🔹 Enter YouTube Channel ID")

channel_id = st.text_input(
    "YouTube Channel ID",
    placeholder="e.g., UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

if st.button("Run Pipeline"):
    if channel_id.strip() == "":
        st.error("Channel ID cannot be empty.")
    else:
        st.info("⏳ Running pipeline… This may take a moment.")

        try:
            df_channel, df_videos, df_comments = run_pipeline(channel_id)
            st.success("🎉 Pipeline completed successfully!")

            st.subheader("Channel Info")
            st.dataframe(df_channel)

            st.subheader("Videos")
            st.dataframe(df_videos)

            st.subheader("Comments")
            st.dataframe(df_comments)

        except Exception as e:
            st.error(f"Pipeline failed: {str(e)}")


# -----------------------------
# FILE UPLOAD
# -----------------------------
st.header("🔹 Upload CSV / Excel Data")

uploaded_file = st.file_uploader(
    "Upload video/comment dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File loaded successfully!")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
