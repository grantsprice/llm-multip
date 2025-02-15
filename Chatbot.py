import openai
import streamlit as st
from streamlit_chat import message

st.title("💬 Council of Advisors GPT")
st.header("Choose your council on the left and ask away!")
openai_api_key = st.secrets["chatbot_api_key"]

with st.sidebar:
        st.header("Configuration")
        options = st.multiselect(
        'Choose your panel of advisors:',
        ['Gandhi', 'Stalin', 'Plato', 'Confucius', 'Karl Marx', 'Epicurus', 'Friedrich Nietzsche', 'Socrates', 'Aristotle', 'Albert Einstein', 'Charles Darwin'],
        ['Gandhi', 'Stalin', 'Plato'])
        btnResult = st.button("Go!")
    
if "messages" not in st.session_state or btnResult:
    st.session_state["messages"] = []
    options_str = ', '.join(options)
    system_message = {
        "role": "system",
        #"content": "Respond as each of these three personas to each prompt: \nPlato: and respond how Plato would respond\nStalin: and respond how Stalin would respond\nGandhi: and respond how Gandhi would respond. You should respond in the first person for each of these three personas.",
        "content": "You are an award winning novelist simulating a conversation between" + options_str + " about the topic or question posed by the user. After the three responses, give one response from one persona to another's answer.",
    }
    st.session_state.messages.append(system_message)

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for idx, msg in enumerate(st.session_state.messages[1:]):
    message(msg["content"], is_user=msg["role"] == "user", key=idx)

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if user_input and openai_api_key:
    openai.api_key = openai_api_key
    model_input_messages = [st.session_state.messages[0]] + [{"role": "user", "content": user_input}]
    message(user_input, is_user=True)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=model_input_messages)
    assistant_response = response.choices[0].message
    st.session_state.messages.append(assistant_response)
    message(assistant_response.content)
