from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get response

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, chat_history):
    try:
        #prev_chat = chat_history + question
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

## initialize our stramlit app

st.set_page_config(page_title="Q&A Chatbot")

st.header("Gemini LLM Conversation Application")
    
# intialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [] 
    
input = st.text_input("Input:", key= "input")
submit = st.button("Ask the question")

if submit and input:
   
    # add user query and response to session chat history
    st.session_state['chat_history'].append(("you",input)) # Append the chat history to the empty list which is declared above.
    chat_history = st.session_state['chat_history'] 
    response = get_gemini_response(input, chat_history)
    st.subheader("The Response is ")
    
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("AI Assistant",chunk.text))
st.subheader("The chat history is ")

if(st.button("Show Chat History")):
    for role,text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
