import requests
import streamlit as st

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Spring AI Docs Assistant",
    page_icon="🤖",
)

st.title("🤖 Spring AI Docs Assistant")

question = st.chat_input("Ask about Spring AI...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            json={"question": question},
        )

    data = response.json()

    with st.chat_message("assistant"):
        st.write(data["answer"])

        if data["sources"]:
            with st.expander("Sources"):
                for source in data["sources"]:
                    st.write(f"- {source}")