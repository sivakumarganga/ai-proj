# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import google.generativeai as genai

# # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# ## function to load gemeni pro model and get response
# model = genai.GenerativeModel("gemini-2.0-flash")

# chat = model.start_chat(history=[])

# def get_gemeni_response(question):
#     response = chat.send_message(question, stream=True)
#     return response

# st.header("Travel Plan Chatbot")
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []
# if 'step' not in st.session_state:
#     st.session_state['step'] = 0
# if 'origin' not in st.session_state:
#     st.session_state['origin'] = ""
# if 'destination' not in st.session_state:
#     st.session_state['destination'] = ""

# def ask_question(prompt):
#     st.session_state['chat_history'].append(("Bot", prompt))
#     st.session_state['step'] += 1

# if st.session_state['step'] == 0:
#     ask_question("Where are you traveling from?")
# elif st.session_state['step'] == 1:
#     user_input = st.text_input("Origin:", key="origin_input")
#     submit = st.button("Send Origin")
#     if submit and user_input:
#         st.session_state['origin'] = user_input
#         st.session_state['chat_history'].append(("You", user_input))
#         ask_question("Where are you traveling to?")
# elif st.session_state['step'] == 2:
#     user_input = st.text_input("Destination:", key="destination_input")
#     submit = st.button("Send Destination")
#     if submit and user_input:
#         st.session_state['destination'] = user_input
#         st.session_state['chat_history'].append(("You", user_input))
#         ask_question("What is your purpose?")
# elif st.session_state['step'] == 3:
#     user_input = st.text_input("Purpose:", key="destination_input")
#     submit = st.button("Send Purpose")
#     if submit and user_input:
#         st.session_state['purpose'] = user_input
#         st.session_state['chat_history'].append(("You", user_input))
#         ask_question("What is your purpose?")
# elif st.session_state['step'] == 4:
#         user_input = st.text_input("Days: ", key= "travel_days_input")
#         submit = st.button("Send Days")
#         if submit and user_input:
#             st.session_state['days'] = user_input
#             st.session_state['chat_history'].append(("You", user_input))
#             ask_question("What are you your interest?")
# elif st.session_state['step'] == 5:
#         user_input = st.text_input("Interests: ", key= "travel_interests_input")
#         submit = st.button("Send Interests")
#         if submit and user_input:
#             st.session_state["interests"] = user_input
#             st.session_state["chat_history"].append(("You", user_input))
#             ask_question("What is your budget?")
# elif st.session_state['step'] == 6:
#         user_input = st.text_input("Budget: ", key= "budget_input")
#         submit = st.button("Send Budget")
#         if submit and user_input:
#             st.session_state['budget'] = user_input
#             st.session_state['chat_history'].append(("You", user_input))
#         # TODO: Generate travel plan using Gemini AI
#         question = f"Generate a travel plan from {st.session_state['origin']} to {st.session_state['destination']}."
#         response = get_gemeni_response(question)
#         resp = ""
#         for chunk in response:
#             resp += chunk.text
#         st.session_state['chat_history'].append(("Bot", resp))
#         st.session_state['step'] += 1

# st.subheader("The chat history is : ")
# for role, text in st.session_state['chat_history']:
#     st.write(f"{role} : {text}")


from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print(os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

chat = model.start_chat(history=[])

def get_gemeni_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.markdown(
    """
    <style>
    .fade-in {
        animation: fadeIn ease 2s;
        -webkit-animation: fadeIn ease 2s;
        -moz-animation: fadeIn ease 2s;
        -o-animation: fadeIn ease 2s;
        -ms-animation: fadeIn ease 2s;
    }
    @keyframes fadeIn {
        0% {opacity:0;}
        100% {opacity:1;}
    }

    </style>
    """,
    unsafe_allow_html=True,)
st.markdown("<h1 class='fade-in'>Travel Plan Chatbot</h1>", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'step' not in st.session_state:
    st.session_state['step'] = 0
if 'origin' not in st.session_state:
    st.session_state['origin'] = ""
if 'destination' not in st.session_state:
    st.session_state['destination'] = ""
if 'travel_days' not in st.session_state:
    st.session_state['travel_days'] = ""
if 'travel_interests' not in st.session_state:
    st.session_state['travel_interests'] = ""
if 'budget' not in st.session_state:
    st.session_state['budget'] = ""

def ask_question(prompt):
    st.session_state['chat_history'].append(("Bot", prompt))
    st.session_state['step'] += 1

if st.session_state['step'] == 0:
    ask_question("Where are you traveling from?")
elif st.session_state['step'] == 1:
    user_input = st.text_input("Origin:", key="origin_input")
    submit = st.button("Send Origin")
    if submit and user_input:
        st.session_state['origin'] = user_input
        st.session_state['chat_history'].append(("You", user_input))
        ask_question("Where are you traveling to?")
elif st.session_state['step'] == 2:
    user_input = st.text_input("Destination:", key="destination_input")
    submit = st.button("Send Destination")
    if submit and user_input:
        st.session_state['destination'] = user_input
        st.session_state['chat_history'].append(("You", user_input))
        ask_question("What is you purpose?")
elif st.session_state['step'] == 3:
    user_input = st.text_input("Purpose:", key="purpose_input")
    submit = st.button("Send Purpose")
    if submit and user_input:
        st.session_state['purpose'] = user_input
        st.session_state['chat_history'].append(("You", user_input))
        ask_question("How many days do you plan to travel?")
elif st.session_state['step'] == 4:
    user_input = st.text_input("Travel Days:", key="travel_days_input")
    submit = st.button("Send Travel Days")
    if submit and user_input:
        st.session_state['travel_days'] = user_input
        st.session_state['chat_history'].append(("You", user_input))
        ask_question("What are your interests (e.g., food, history, nature)?")
elif st.session_state['step'] == 5:
    user_input = st.text_input("Interests:", key="interests_input")
    submit = st.button("Send Interests")
    if submit and user_input:
        st.session_state['travel_interests'] = user_input
        st.session_state['chat_history'].append(("You", user_input))
        ask_question("What is your approximate budget?")
elif st.session_state['step'] == 6:
    user_input = st.text_input("Budget:", key="budget_input")
    submit = st.button("Send Budget")
    if submit and user_input:
        st.session_state['budget'] = user_input
        st.session_state['chat_history'].append(("You", user_input))
        ask_question("Please wait while I generate your personalized travel plan...")
        question = f"""
"Create a travel plan from {st.session_state['origin']} to {st.session_state['destination']} for {st.session_state['travel_days']} days. The purpose of this trip is {st.session_state['purpose']}.
Provide the following information in a clear and organized format, using headings and bullet points, and include clickable links using Markdown format:
1.  A general travel itinerary, without detailed daily schedules.
2.  A list of required travel documents, including estimated costs where applicable, and a purchase link for each document.
3.  Travel tips specifically related to the purpose of the trip.
4.  A list of 3 recommended hotels at various price points within the budget of {st.session_state['budget']}, including price ranges and booking links.
5.  A list of 5 activities based on the following interests: {st.session_state['travel_interests']}, including descriptions and official website links.
"""
        response = get_gemeni_response(question)
        resp = ""
        for chunk in response:
            resp += chunk.text
        st.session_state['chat_history'].append(("Bot", resp))
        st.session_state['step'] += 1

st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")