from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load gemeni pro model and get response
model = genai.GenerativeModel("gemini-2.0-flash")

chat = model.start_chat(history=[])

def get_gemeni_response(question):
    system_prompt = "You are an International Travel Desk/Agent. Provide detailed and well-structured travel plans in short."
    response = chat.send_message(f"{system_prompt}\n{question}", stream=True)
    return response

st.header("Your Travel Desk Chatbot")

# Button to clear session state
if st.button("Restart Chatbot"):
    st.session_state.clear()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 0
if 'origin' not in st.session_state:
    st.session_state['origin'] = ""
if 'destination' not in st.session_state:
    st.session_state['destination'] = ""

def ask_question(prompt):
    st.session_state['chat_history'].append(("Bot", prompt))
    st.session_state['step'] += 1

if st.session_state['step'] == 0:
    ask_question("Where are you traveling from?")
elif st.session_state['step'] == 1:
    with st.form(key='origin_form'):
        user_input = st.text_input("Origin:", key="origin_input")
        submit = st.form_submit_button("Send Origin")
        if submit and user_input:
            st.session_state['origin'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("Where are you traveling to?")
elif st.session_state['step'] == 2:
    with st.form(key='destination_form'):
        user_input = st.text_input("Destination:", key="destination_input")
        submit = st.form_submit_button("Send Destination")
        if submit and user_input:
            st.session_state['destination'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("Please wait while I generate your travel plan...")
            # Generate travel plan using Gemini AI
            question = f"Generate a travel plan from {st.session_state['origin']} to {st.session_state['destination']}."
            response = get_gemeni_response(question)
            resp = ""
            for chunk in response:
                resp += chunk.text
            st.session_state['chat_history'].append(("Bot", resp))
            st.session_state['step'] += 1

st.subheader("The chat history is : ")
for role, text in st.session_state['chat_history']:
    st.write(f"{role} : {text}")