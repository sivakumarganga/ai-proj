from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from streamlit_chat import message

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

def get_gemeni_response(question):
    system_prompt = f"""
        "You are an International Travel Expert. Provide detailed and well-structured travel plans, with weather chart comparison from origin and destination..
        Provide the following information in a clear and organized format, using headings and bullet points, and include clickable links using Markdown format:
        1.  A general travel itinerary, without detailed daily schedules.
        2.  A list of required travel documents, including estimated costs where applicable, and a purchase link for each document.
        3.  Travel tips specifically related to the purpose of the trip.
        4.  A list of 3 recommended hotels at various price points within the budget, including price ranges and booking links.
        """
    response = chat.send_message(f"{system_prompt}\n{question}", stream=True)
    return response

st.header("Your Travel Desk Chatbot")

# Button to clear session state
if st.button("Restart Chatbot"):
    st.session_state.clear()
    st.rerun()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 0
if 'origin' not in st.session_state:
    st.session_state['origin'] = ""
if 'destination' not in st.session_state:
    st.session_state['destination'] = ""
if 'state' not in st.session_state:
    st.session_state['state'] = ""
if 'visa' not in st.session_state:
    st.session_state['visa'] = ""
if 'plans' not in st.session_state:
    st.session_state['plans'] = ""
if 'budget' not in st.session_state:
    st.session_state['budget'] = ""


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
            st.rerun()
elif st.session_state['step'] == 2:
    with st.form(key='destination_form'):
        user_input = st.text_input("Destination:", key="destination_input")
        submit = st.form_submit_button("Send Destination")
        if submit and user_input:
            st.session_state['destination'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("Which specific state are you traveling to, if not already mentioned?")
            st.rerun()
elif st.session_state['step'] == 3:
    with st.form(key='state_form'):
        user_input = st.text_input("State:", key="state_input")
        submit = st.form_submit_button("Send State")
        if submit and user_input:
            st.session_state['state'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("What type of visa do you own and what are your plans for the visit?")
            st.rerun()
elif st.session_state['step'] == 4:
    with st.form(key='visa_form'):
        user_input = st.text_input("Visa and Plans:", key="visa_input")
        submit = st.form_submit_button("Send Visa and Plans")
        if submit and user_input:
            st.session_state['visa'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("What are your plans for air travel and staying?")
            st.rerun()
elif st.session_state['step'] == 5:
    with st.form(key='plans_form'):
        user_input = st.text_input("Air Travel and Staying Plans:", key="plans_input")
        submit = st.form_submit_button("Send Plans")
        if submit and user_input:
            st.session_state['plans'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("What is your budget for travel?")
            st.rerun()
elif st.session_state['step'] == 6:
    with st.form(key='budget_form'):
        user_input = st.text_input("Budget:", key="budget_input")
        submit = st.form_submit_button("Send Budget")
        if submit and user_input:
            st.session_state['budget'] = user_input
            st.session_state['chat_history'].append(("You", user_input))
            ask_question("Please wait while I generate your travel plan...")
            # Generate travel plan using Gemini AI
            question = f"Generate a travel plan from {st.session_state['origin']} to {st.session_state['destination']} in {st.session_state['state']}. Visa: {st.session_state['visa']}. Plans: {st.session_state['plans']}. Budget: {st.session_state['budget']}."
            response = get_gemeni_response(question)
            resp = ""
            for chunk in response:
                resp += chunk.text
            st.session_state['chat_history'].append(("Bot", resp))
            st.session_state['step'] += 1
            st.rerun()

# Upload itinerary document
uploaded_file = st.file_uploader("Upload your itinerary document", type=["txt", "pdf", "docx"])
if uploaded_file is not None:
    # Process the uploaded file
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    st.write(file_details)
    # Read the file content
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        import PyPDF2
        reader = PyPDF2.PdfFileReader(uploaded_file)
        content = ""
        for page in range(reader.numPages):
            content += reader.getPage(page).extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx
        doc = docx.Document(uploaded_file)
        content = "\n".join([para.text for para in doc.paragraphs])
    st.text_area("Itinerary Content", content, height=300)

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    if role == "Bot":
        message(text, is_user=False)
    else:
        message(text, is_user=True)
