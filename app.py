import streamlit as st
import PyPDF2
from groq import Groq
import os
from dotenv import load_dotenv

# 1. .env file-la irukra keys-a load pannuvom
load_dotenv() 

# 2. .env-la irundhu key-a eduthu 'api_key' nu store panrom
api_key = os.getenv("GROQ_API_KEY")

# 3. 🔑 Groq API - Inga dhaan fix panni irukken
if api_key:
    # Munnadi GROQ_API_KEY nu irundhadha ippo api_key nu mathi irukken
    client = Groq(api_key=api_key) 
else:
    st.error("API Key missing! Please check your .env file.")
    st.stop()

# --- Matha functions ellam adhae dhaan ---

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def analyze_document(text):
    prompt = f"""
     You are an AI document analysis expert.

    Provide:

    1. Summary (short and clear)
        2.Identify the categories and display it
        3. Stakeholders
         (● Which stakeholders benefit
          ● Which stakeholders face constraints
          ● New academic or institutional opportunities)
        3. Impact Assessment
         (● Short term ((immediate effects in schools, colleges, administration)
          ● Medium term (Growth + stability)
          ● Long term ((future effects over time))
        4. Impact Analyzer
        5.Awareness & Academic Support
        6.Risks (possible problems, challenges, or negative effects)
        7.Positive and Negative
        8.Governance & Compliance.
    Document:
    {text}
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-safeguard-20b", 
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 🎯 STREAMLIT UI
st.set_page_config(page_title="AI PDF Analyzer", layout="wide")
st.title("📄 AI PDF Document Analyzer")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")
    text = extract_text(uploaded_file)

    if st.button("Analyze Document 🚀"):
        if text.strip() == "":
            st.warning("The PDF seems to be empty or unscannable.")
        else:
            with st.spinner("Analyzing with AI..."):
                try:
                    result = analyze_document(text)
                    st.subheader("📊 Analysis Result")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")