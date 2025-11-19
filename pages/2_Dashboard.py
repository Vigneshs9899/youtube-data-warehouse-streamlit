import streamlit as st
import pandas as pd
import plotly.express as px
from db_read import load_channels, load_videos, load_comments

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

st.title("📊 YouTube Analytics Dashboard")

# Load Data from Neon PostgreSQL
channels_df = load_channels()

if channels_df.empty:
    st.error("❌ No channels found in database. Please run the Import Data page first.")
    st.stop()

# Sidebar
st.sidebar.header("Filters")
section = st.sidebar.radio("Select analysis", ["Channel Stats", "Video Analytics", "Comments Analytics"])

# -------------------------
# CHANNEL STATS
# -------------------------
if section == "Channel Stats":
    st.header("📌 Channel Overview")

    selected_channel = st.selectbox(
        "Select Channel",
        channels_df["channel_id"]
    )

    ch = channels_df[channels_df["channel_id"] == selected_channel]

    col1, col2, col3 = st.columns(3)
    col1.metric("Subscribers", int(ch["subscriber_count"].iloc[0]))
    col2.metric("Views", int(ch["view_count"].iloc[0]))
    col3.metric("Videos", int(ch["video_count"].iloc[0]))

    st.dataframe(ch)

# -------------------------
# VIDEO ANALYTICS
# -------------------------
elif section == "Video Analytics":
    st.header("🎬 Video Metrics")

    selected_channel = st.selectbox(
        "Select Channel",
        channels_df["channel_id"]
    )

    df_videos = load_videos(selected_channel)

    st.subheader("Video List")
    st.dataframe(df_videos)

    st.subheader("Views Over Time")
    fig = px.line(df_videos, x="published_at", y="viewCount", title="Views Over Time")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# COMMENTS ANALYTICS
# -------------------------
elif section == "Comments Analytics":
    st.header("💬 Comments Overview")

    selected_channel = st.selectbox(
        "Select Channel",
        channels_df["channel_id"]
    )

    df_videos = load_videos(selected_channel)
    video_list = df_videos["video_id"].tolist()

    selected_video = st.selectbox("Select Video", video_list)

    df_comments = load_comments(selected_video)

    st.dataframe(df_comments)

    top_authors = df_comments["author"].value_counts().head(10)
    st.subheader("Top Commenters")
    st.bar_chart(top_authors)
