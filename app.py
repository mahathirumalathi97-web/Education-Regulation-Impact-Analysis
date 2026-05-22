import streamlit as st
import PyPDF2
from groq import Groq

# 🔑 Groq API
client = Groq(api_key="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")

# 📄 Extract text from PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# 🤖 AI Analysis Function
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
        8.Governance & Compliance

    Document:
    {text}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-safeguard-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# 🎯 STREAMLIT UI
st.title("📄 AI PDF Document Analyzer")
st.write("Upload a PDF to get AI-powered analysis")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:

    st.success("PDF Uploaded Successfully!")

    # Extract text
    text = extract_text(uploaded_file)

    if st.button("Analyze Document 🚀"):

        with st.spinner("Analyzing with AI..."):
            result = analyze_document(text)

        st.subheader("📊 Analysis Result")
        st.write(result)
