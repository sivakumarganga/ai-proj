import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar allows a list of past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    # Save new chats after a message has been sent to AI
    # TODO: Give user a chance to name chat
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

st.write('# Your Travel Desk Chatbot')

# Travel details input
st.write('## Travel Details')
travel_from = st.text_input('Traveling from (Given)')
destination = st.text_input('Destination (Given)')
specific_state = st.text_input('Specific State needed if not already mentioned')
visa_type = st.text_input('Type of Visa owned and plans for visit')
air_travel_plans = st.text_input('Plans for Air travel and staying')
travel_budget = st.text_input('Budget for travel?')

# Chat history (allows to ask multiple questions)
try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
    print('old cache')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    print('new_cache made')
st.session_state.model = genai.GenerativeModel('gemini-2.0-flash')
st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Your message here...'):
    # Save this as a chat for later
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(f"Traveling from: {travel_from}\nDestination: {destination}\nSpecific State: {specific_state}\nVisa Type: {visa_type}\nAir Travel Plans: {air_travel_plans}\nTravel Budget: {travel_budget}\n\n{prompt}")
    # Add user message to chat history
    st.session_state.messages.append(
        dict(
            role='user',
            content=f"Traveling from: {travel_from}\nDestination: {destination}\nSpecific State: {specific_state}\nVisa Type: {visa_type}\nAir Travel Plans: {air_travel_plans}\nTravel Budget: {travel_budget}\n\n{prompt}",
        )
    )
    # Send message to AI
   
    ai_prompt = (
        "ou are an International Travel Expert. Provide detailed and well-structured travel plans, with weather chart comparison from origin and destination..\n\n"
        "Provide the following information in a clear and organized format, using headings and bullet points, and include clickable links using Markdown format:\n\n"
        "1. A general travel itinerary, without detailed daily schedules.\n\n"
        "2. A list of required travel documents, including estimated costs where applicable, and a purchase link for each document.\n\n"
        "3. Travel tips specifically related to the purpose of the trip.\n\n"
        "4. A list of 3 recommended hotels at various price points within the budget, including price ranges and booking links.\n\n"
        f"Traveling from: {travel_from}\nDestination: {destination}\nSpecific State: {specific_state}\n"
        f"Visa Type: {visa_type}\nAir Travel Plans: {air_travel_plans}\nTravel Budget: {travel_budget}\n\n{prompt}"
    )
    response = st.session_state.chat.send_message(
        ai_prompt,
        stream=True,
    )
    # Display assistant response in chat message container
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                # Rewrites with a cursor at end
                message_placeholder.write(full_response + '▌')
        # Write full message with placeholder
        message_placeholder.write(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    # Save to file
    joblib.dump(
        st.session_state.messages,
        f'data/{st.session_state.chat_id}-st_messages',
    )
    joblib.dump(
        st.session_state.gemini_history,
        f'data/{st.session_state.chat_id}-gemini_messages',
    )