import streamlit as st
import plotly.express as px
from db_read import load_channels, load_videos, load_comments

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

st.title("📊 YouTube Analytics Dashboard")
st.write("Analyze channel, video, and comment data from PostgreSQL.")

# ----------------------------
# SIDEBAR: CHANNEL SELECTOR
# ----------------------------
st.sidebar.header("Filters")

channels_df = load_channels()

if channels_df.empty:
    st.error("❌ No channels found in database. Please run the data pipeline first.")
    st.stop()

channel_ids = channels_df["channel_id"].tolist()

selected_channel = st.sidebar.selectbox(
    "Select YouTube Channel",
    options=channel_ids
)

# Load data for selected channel
videos_df = load_videos(selected_channel)
comments_df = load_comments()

# ----------------------------
# NAVIGATION
# ----------------------------
section = st.sidebar.radio(
    "Select a section",
    ["Channel Stats", "Video Analytics", "Comments Analytics"]
)


# ------------------------------------------------
# 1️⃣ CHANNEL STATS
# ------------------------------------------------
if section == "Channel Stats":
    st.header("📌 Channel Overview")

    channel_info = channels_df[channels_df["channel_id"] == selected_channel]

    if channel_info.empty:
        st.warning("No data found for this channel.")
    else:
        ch = channel_info.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric("Subscribers", ch['subscriber_count'])
        col2.metric("Total Views", ch['view_count'])
        col3.metric("Total Videos", ch['video_count'])

        st.subheader("Channel Details")
        st.dataframe(channel_info, use_container_width=True)



# ------------------------------------------------
# 2️⃣ VIDEO ANALYTICS
# ------------------------------------------------
elif section == "Video Analytics":
    st.header("🎬 Video Metrics")

    if videos_df.empty:
        st.warning("No video data available for this channel.")
    else:
        st.subheader("Video List")
        st.dataframe(videos_df, use_container_width=True)

        # Convert date
        videos_df["published_at"] = videos_df["published_at"].astype(str)

        # Views Trend
        st.subheader("📈 Views Over Time")
        fig = px.line(videos_df, x="published_at", y="view_count", title="Views Over Time")
        st.plotly_chart(fig, use_container_width=True)

        # Top Videos
        st.subheader("🔥 Top Videos by Views")
        top_vids = videos_df.sort_values("view_count", ascending=False).head(10)
        fig2 = px.bar(top_vids, x="title", y="view_count", title="Top 10 Videos")
        st.plotly_chart(fig2, use_container_width=True)



# ------------------------------------------------
# 3️⃣ COMMENTS ANALYTICS
# ------------------------------------------------
elif section == "Comments Analytics":
    st.header("💬 Comments Overview")

    if comments_df.empty:
        st.warning("No comments available.")
    else:
        st.subheader("All Comments")
        st.dataframe(comments_df, use_container_width=True)

        # Top commenters
        st.subheader("🏆 Top 10 Active Commenters")
        top_authors = comments_df['author_name'].value_counts().head(10)
        st.bar_chart(top_authors)

        # Comments per video
        st.subheader("💬 Comments per Video")
        comment_counts = comments_df.groupby("video_id").size().reset_index(name="total_comments")

        merged = videos_df.merge(comment_counts, on="video_id", how="left")
        merged["total_comments"].fillna(0, inplace=True)

        fig3 = px.bar(
            merged,
            x="title",
            y="total_comments",
            title="Comments per Video"
        )
        st.plotly_chart(fig3, use_container_width=True)
