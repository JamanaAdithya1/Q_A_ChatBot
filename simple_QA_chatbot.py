from dotenv import load_dotenv # Load environment variables.
load_dotenv()

import streamlit as st # UI Interface 
import os 
import google.generativeai as genai # Loading gemini pro API

geminiAPIkey = os.getenv("google_API_key")
genai.configure(api_key = geminiAPIkey) # Load my API key

model = genai.GenerativeModel("gemini-pro") # Specify the gemini model to use 

chat = model.start_chat()

def get_Gemini_Response(question):
    try: 
        response = chat.send_message(question, stream = True) # Sending a request to API and storing the response in "response" variable
        return response
    except Exception as e:
        return f"An error Occured: {e}"
    

# Code for Web UI
st.set_page_config(page_title = "Q and A ChatBot")
st.header("Q and A ChatBot")

input = st.text_input("question", key = "input")
submit = st.button("Ask the question")

if(input and submit) : 
    response = get_Gemini_Response(input) # Call gemini response for the given input
    # st.subheader("The response is")
    for chunk in response: 
        st.write(chunk.text)