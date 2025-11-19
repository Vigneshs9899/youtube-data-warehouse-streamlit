import streamlit as st
import pandas as pd
from pipeline import run_pipeline
from db_insert import insert_videos, insert_comments, insert_channel

st.set_page_config(page_title="YouTube Data Loader", layout="centered")

st.title("📥 YouTube Channel Data Loader & Uploader")


# =====================================================
#  SECTION 1 — CHANNEL ID INPUT & AUTOMATED API FETCH
# =====================================================
st.header("🔹 Enter YouTube Channel ID (Auto Fetch & Save)")

channel_id = st.text_input(
    "YouTube Channel ID",
    placeholder="e.g., UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

if st.button("Fetch from YouTube API"):
    if channel_id.strip() == "":
        st.error("Channel ID cannot be empty.")
    else:
        st.info("Fetching from YouTube API... Please wait ⏳")

        try:
            df_channel, df_videos, df_comments = run_pipeline(channel_id)

            st.success("🎉 Data fetched and saved to PostgreSQL successfully!")

            st.subheader("📌 Channel Info")
            st.dataframe(df_channel)

            st.subheader("📼 Videos Preview")
            st.dataframe(df_videos.head())

            st.subheader("💬 Comments Preview")
            st.dataframe(df_comments.head())

        except Exception as e:
            st.error(f"❌ Error: {e}")


st.markdown("---")


# =====================================================
#   SECTION 2 — MANUAL FILE UPLOAD (CSV / Excel)
# =====================================================
st.header("🔹 Upload CSV or Excel (Manual Data Insert)")

uploaded_file = st.file_uploader(
    "Upload video/comment dataset",
    type=["csv", "xlsx"],
    accept_multiple_files=False
)

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    st.info(f"Uploaded file: **{uploaded_file.name}**")

    try:
        # Read file
        if file_ext == "csv":
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File loaded successfully!")
        st.dataframe(df)

        # -------------------------
        # Insert uploaded data
        # -------------------------
        if st.button("Save Uploaded Data to Database"):
            try:
                if "video_id" in df.columns:
                    insert_videos(df)
                    st.success("Videos inserted into DB!")

                if "comment_id" in df.columns:
                    insert_comments(df)
                    st.success("Comments inserted into DB!")

                if "channel_id" in df.columns and "title" in df.columns:
                    insert_channel(df)
                    st.success("Channel data inserted!")

            except Exception as e:
                st.error(f"DB Insert Error: {e}")

    except Exception as e:
        st.error(f"Error reading file: {e}")


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("⚡ Phase 7 — Streamlit Integrated with API + Database 🚀")
