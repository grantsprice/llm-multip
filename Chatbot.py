import openai
import streamlit as st
from streamlit_chat import message

st.title("💬 Multip GPT")
openai_api_key = st.secrets["chatbot_api_key"]
if "messages" not in st.session_state:
    st.session_state["messages"]= [{"role": "system", "content": "Respond as each of these three personas to each prompt: \nPlato: and respond how plato would respond\nStalin: and respond how Stalin would respond\nGandhi: and respond how Gandhi would respond."}]
    st.session_state.messages.append({"role": "assistant", "content": "How can I help you?"})

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for idx, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=idx)

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if user_input and openai_api_key:
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
