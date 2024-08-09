import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
import cohere

# Cohere API Key
co = cohere.Client('4FKKMVQ8Waw0IE3QmmX5CMPWL2mAm8hya8zpoSNT')

# Custom CSS for attractive design and animations
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    h1 {
        text-align: center;
        color: #4b8bbe;
        font-family: 'Arial', sans-serif;
        font-size: 3rem;
        font-weight: bold;
        animation: colorChange 3s infinite alternate;
    }
    .stButton>button {
        background-color: #4b8bbe;
        color: white;
        font-size: 1.2rem;
        padding: 0.5em 2em;
        border-radius: 10px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357ab7;
    }
    .stFileUploader {
        text-align: center;
        margin-top: 2rem;
        font-size: 1.1rem;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
        font-size: 1.2rem;
        background: linear-gradient(to right, #a6c1ee, #fbc2eb);
        -webkit-background-clip: text;
        color: transparent;
    }
    @keyframes colorChange {
        from { color: #4b8bbe; }
        to { color: #f77062; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

def extract_text_from_pdf(pdf_path):
    """Extract text from the given PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text


pytesseract.pytesseract.tesseract_cmd = r'D:\SoftwareFiles\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image):
    """Extract text from the given image using OCR."""
    text = pytesseract.image_to_string(image)
    return text

def extract_details(text):
    """Extract customer details, products, and total amount using Cohere API."""
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=f"Extract customer details, products, and total amount from this invoice:\n{text}",
        max_tokens=150
    )
    return response.generations[0].text.strip()

def main():
    """Main function to handle Streamlit app logic."""
    st.title("Invoice Data Extraction")

    # File uploader for PDF and Image
    uploaded_file = st.file_uploader("Upload Invoice (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            image = Image.open(uploaded_file)
            text = extract_text_from_image(image)

        details = extract_details(text)
        st.subheader("Extracted Details")
        st.write(details)

if __name__ == "__main__":
    main()
