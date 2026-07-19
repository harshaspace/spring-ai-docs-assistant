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

                request_id = data["request_id"]

                if data.get("sources"):
                    with st.expander("Sources"):
                        for source in data["sources"]:
                            st.write(f"📄 {source}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍 Helpful"):
                        requests.post(
                            "http://api:8000/feedback", 
                            json={
                                "request_id": request_id,
                                "feedback": "up",
                                },
                        )
                        st.success("Thanks for your feedback!")

                with col2:
                    if st.button("👎 Not Helpful"):
                        requests.post(
                            "http://api:8000/feedback", 
                            json={
                                "request_id": request_id,
                                "feedback": "down",
                                },
                        )
                        st.success("Thanks for your feedback!")

            except requests.exceptions.RequestException as ex:
                st.error(f"Unable to connect to the API.\n\n{ex}")