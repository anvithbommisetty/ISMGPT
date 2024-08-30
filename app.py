from main import answer_query 
import streamlit as st
from chat_history import modify_chat_history, convert_to_streamlit

# Set the page configuration
st.set_page_config(page_title="ISMGPT")

# Add a main title
st.title("ISMGPT Chatbot")

# Add a header
st.header("Welcome to the ISMGPT Chatbot")
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am a student at IIT ISM Dhanbad. How can I help you today?"}]

if "LOG" not in st.session_state:
    st.session_state.LOG = [{"role": "assistant", "content": "Hello! I am a student at IIT ISM Dhanbad. How can I help you today?"}]  
    
for message in st.session_state.LOG:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        history = modify_chat_history(st.session_state.messages)
        response = answer_query(prompt, history) 
        message_placeholder.markdown(response)
    st.session_state.messages = convert_to_streamlit(history)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.LOG.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.LOG.append({"role": "assistant", "content": response})