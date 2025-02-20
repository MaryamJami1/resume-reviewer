import os
import streamlit as st
import fitz  
from openai import OpenAI
from dotenv import load_dotenv

#  Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API Key is missing! Add it to the .env file.")
    st.stop()

#  Initialize OpenAI client
client = OpenAI(api_key=api_key)

#  Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

#  Function to analyze resume
def analyze_resume(resume_text):
    prompt = f"""
    Analyze this resume and provide:
    1. A score (1-10) based on content quality.
    2. Strengths and weaknesses.
    3. Improvement suggestions.

    Resume Text:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# 🎨 **Streamlit UI**
st.title("📄 AI Resume Reviewer")
st.write("Upload your resume (PDF), and AI will analyze it!")

#  File uploader
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success(" Resume uploaded successfully!")
    
    with st.spinner("🔍 Analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        feedback = analyze_resume(resume_text)

    st.subheader("🔎 AI Feedback")
    st.write(feedback)
