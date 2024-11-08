
# Import libraries
import os
import streamlit as st
import pandas as pd
import requests
from googletrans import Translator  # For multilingual support

# Initialize the translator for multilingual support
translator = Translator()

# Set your Groq API key here
GROQ_API_KEY = "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"  # Replace with your actual Groq API key

### 1. LOAD DATASET FOR RAG IMPLEMENTATION ###

# Load dataset directly
def load_dataset(file_path="/content/drive/MyDrive/updated_tourist-destinations-in-pakistan-1.0.xlsx"):
    try:
        dataset = pd.read_csv(file_path, encoding='latin1')  # Adjust encoding as needed
        return dataset
    except UnicodeDecodeError:
        st.error("There was an issue loading the dataset due to encoding. Try using a different encoding format.")
        return None

# RAG Function: Retrieve relevant information from dataset based on user query
def retrieve_data(query, dataset):
    results = dataset[dataset.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        return results.to_string()
    else:
        return "Sorry, no relevant information found in the dataset."

### 2. GENERAL CHATBOT FEATURES ###

# Function for greeting and introduction
def greet_user():
    return "Welcome! I am your virtual tour guide for Pakistan. How can I assist you today?"

# Function for user preferences and personalized recommendations
def get_user_preferences():
    st.text_input("Enter your preferred city:")
    st.number_input("Enter your travel duration in days:")
    st.text_input("Enter your interests (e.g., culture, food, etc.):")
    st.number_input("Enter your budget range:")

# Function to give tourist tips and FAQs
def provide_tips():
    return "Here are some tips: Stay hydrated, try local food, respect local customs, and keep your belongings safe."

# Function to handle questions regarding accommodation
def accommodation_recommendations(city):
    return f"Recommended accommodations in {city}: Hotel XYZ, Guesthouse ABC."

# Function to provide traffic and transport details
def transport_info(city):
    return f"Current traffic situation in {city}: Moderate. Here are the transport options..."

### 3. MAIN CHATBOT LOGIC WITH RAG INTEGRATION ###

def chatbot_interaction(dataset):
    user_input = st.text_input("Ask a question or type 'help' for more info:")

    if user_input.lower() == "help":
        st.write(greet_user())
        st.write(provide_tips())
    elif user_input.lower().startswith("accommodation"):
        city = user_input.split(" ")[1]
        st.write(accommodation_recommendations(city))
    elif user_input.lower().startswith("transport"):
        city = user_input.split(" ")[1]
        st.write(transport_info(city))
    else:
        # Use RAG to retrieve specific responses from the uploaded dataset
        st.write(retrieve_data(user_input, dataset) if dataset is not None else "Please check the dataset file path and encoding.")

### 4. STREAMLIT DEPLOYMENT ###

def deploy_chatbot():
    st.title("Pakistan Tourist Guide Chatbot")
    st.write("Hello! I'm here to help you explore Pakistan.")

    # Load dataset for RAG-based responses
    dataset = load_dataset("/content/drive/MyDrive/updated_tourist-destinations-in-pakistan-1.0.xlsx")  # Set your dataset file path here
    chatbot_interaction(dataset)
