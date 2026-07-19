import os

import requests
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/chat",
)

st.set_page_config(
    page_title="Spring AI Docs Assistant",
    page_icon="🤖",
)

st.title("🤖 Spring AI Docs Assistant")
st.caption("Ask questions about the Spring AI documentation.")

question = st.chat_input("Ask a question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                st.write(data["answer"])

                if data.get("sources"):
                    with st.expander("Sources"):
                        for source in data["sources"]:
                            st.write(f"📄 {source}")

            except requests.exceptions.RequestException as ex:
                st.error(f"Unable to connect to the API.\n\n{ex}")