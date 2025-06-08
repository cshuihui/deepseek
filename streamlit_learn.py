import streamlit as st

st.title("欢迎来到提瓦特")
user_input = '11'
with st.chat_message("user"):
    st.write(user_input)