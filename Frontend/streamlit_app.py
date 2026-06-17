import streamlit as st
import requests

st.set_page_config(
    page_title="AWS Agreement RAG Assistant",
    layout="wide"
)

st.title("AWS Agreement RAG Assistant")

st.markdown(
    """
Ask questions about the AWS Customer Agreement using a
Retrieval-Augmented Generation (RAG) system.
"""
)

# Session State

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Question Input

question = st.chat_input(
    "Ask a question about the AWS Agreement..."
)

if question:

    try:

        with st.spinner(
            "Searching document..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": question
                }
            )

            result = response.json()

            answer = result["answer"]

            sources = result["sources"]

        # Store Question & Answer History

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer,
                "sources": sources
            }
        )

    except requests.exceptions.ConnectionError:

        st.error(
            """
FastAPI server is not running.

Run:

uvicorn app.main:app --reload
"""
        )

# Question & Answer History

if st.session_state.chat_history:

    st.divider()

    for item in reversed(
        st.session_state.chat_history
    ):

        with st.container():

            st.markdown(
                f"#### Question\n{item['question']}"
            )

            st.markdown(
                f"#### Answer\n{item['answer']}"
            )

            with st.expander(
                "Sources"
            ):

                for source in item["sources"]:

                    st.write(source)

            st.divider()

# Analytics

st.subheader("Analytics")

if st.button("View Analytics"):

    try:

        response = requests.get(
            "http://127.0.0.1:8000/analytics"
        )

        analytics = response.json()

        st.markdown(
            "### Most Frequent Questions"
        )

        for item in analytics[
            "most_frequent_questions"
        ]:

            st.write(
                f"• {item[0]} ({item[1]} times)"
            )

        st.markdown(
            "### Unanswered Queries"
        )

        for item in analytics[
            "unanswered_queries"
        ]:

            st.write(
                f"• {item[0]}"
            )

        st.markdown(
            "### Average Response Latency"
        )

        st.metric(
            label="Seconds",
            value=round(
                analytics["average_latency"],
                2
            )
        )

    except requests.exceptions.ConnectionError:

        st.error(
            """
FastAPI server is not running.

Run:

uvicorn app.main:app --reload
"""
        )