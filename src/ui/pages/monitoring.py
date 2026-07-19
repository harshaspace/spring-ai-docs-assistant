import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Monitoring",
    page_icon="📊",
)

st.title("📊 Monitoring Dashboard")

response = requests.get("http://api:8000/metrics")

df = pd.DataFrame(response.json())
if df.empty:
    st.info("No requests have been logged yet.")
    st.stop()



# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ------------------------
# Metrics
# ------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Questions", len(df))

with col2:
    st.metric(
        "Avg Response",
        f"{df['latency'].mean():.0f} ms",
    )

with col3:
    st.metric(
        "Avg Retrieval",
        f"{df['retrieval_latency'].mean():.0f} ms",
    )

with col4:
    st.metric(
        "Avg LLM",
        f"{df['llm_latency'].mean():.0f} ms",
    )

st.divider()

# ------------------------
# Chart 1
# ------------------------

st.subheader("Questions over Time")

questions = (
    df
    .set_index("timestamp")
    .resample("1min")
    .size()
)

st.line_chart(questions)

# ------------------------
# Chart 2
# ------------------------

st.subheader("Response Latency")

st.bar_chart(df["latency"])

# ------------------------
# Chart 3
# ------------------------

st.subheader("Retrieval vs LLM")

st.bar_chart(
    df[
        [
            "retrieval_latency",
            "llm_latency",
        ]
    ]
)

# ------------------------
# Chart 4
# ------------------------

st.subheader("Feedback")

feedback = df["feedback"].fillna("None").value_counts()

st.bar_chart(feedback)

# ------------------------
# Chart 5
# ------------------------

st.subheader("Top Questions")

top_questions = df["question"].value_counts().head(10)

st.bar_chart(top_questions)

# ------------------------
# Raw Data
# ------------------------

st.subheader("Request Log")

st.dataframe(df)