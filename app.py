import streamlit as st
from chat_bot import initialize_chatbot, chat_with_bot

if "chain" not in st.session_state:
    st.session_state.chain = initialize_chatbot()

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Crazy Chatbot!")

# Display history
chat_container = st.container()
with chat_container:
    for message in st.session_state.history:
        if message["role"] == "human":
            role = "You"
            avatar = "👤"
        else:
            role = "Assistant"
            avatar = "🤖"

        chat_box = st.chat_message(role, avatar=avatar)
        chat_box.write(message["content"])

# User input
user_input = st.chat_input("Say something...", key="input")

if user_input:
    if user_input.lower() == "end":
        st.session_state.history.append({"role": "human", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": "Goodbye! Have a great day!"})
        st.rerun()  
    else:
        response, st.session_state.history = chat_with_bot(
            user_input, st.session_state.history, st.session_state.chain, None
        )
        st.rerun()