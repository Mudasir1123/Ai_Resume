import streamlit as st
import google.generativeai as genai
import PyPDF2

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def analyze_resume(text, language="English"):
    try:
        genai.configure(api_key="AIzaSyBBTNFznyQOKaD56pYb-dXxwbp8bGYOXAI")
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        if language == "Urdu":
            prompt = f"یہ ریزیومے کا متن ہے: {text}. اس ریزیومے پر مشورہ فراہم کریں اور بہتری کی تجاویز دیں۔"
        elif language == "Sindhi":
            prompt = f"هي ريزومي جو متن آهي: {text}. هن ريزومي تي مشورو ڏيو ۽ بھتري لاءِ تجويزون پيش ڪريو."
        else:
            prompt = f"This is the resume text: {text}. Provide feedback and suggestions for improvement."
        
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "No feedback available."
    except Exception as e:
        return f"Error analyzing resume: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="📄 AI-Powered Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 AI-Powered Resume Analyzer")
st.write("Upload your resume and get AI-powered feedback!")

# Language selection
language = st.selectbox("🌍 Select language:", ["English", "Urdu", "Sindhi"])

# File uploader
uploaded_file = st.file_uploader("📤 Upload your resume (PDF):", type=["pdf"])

if uploaded_file is not None:
    st.write("📖 Extracting text from resume...")
    resume_text = extract_text_from_pdf(uploaded_file)
    
    if "Error" in resume_text:
        st.error(resume_text)
    else:
        st.success("✅ Resume text extracted successfully!")
        
        if st.button("Analyze Resume"):
            st.write("🤖 Fetching AI feedback...")
            feedback = analyze_resume(resume_text, language)
            st.info(f"📋 AI Resume Feedback: {feedback}")

# Footer
st.markdown("""
    ---
    👨‍💻 Developed by **Muhammad Mudasir**
""", unsafe_allow_html=True)