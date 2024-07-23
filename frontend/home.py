from openai import OpenAI
import streamlit as st


st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div.stSpinner > div {
    text-align:center;
    align-items: center;
    justify-content: center;
    }
    </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .main > .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>""", unsafe_allow_html=True)


st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")





