import streamlit as st
import PyPDF2
import textract
import re

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdf_file as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages
            for page_num in range(num_pages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

# Function to preprocess text
def preprocess_text(text):
    # Remove non-alphanumeric characters and extra spaces
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Convert text to lowercase
    text = text.lower()
    return text

# Main function to run the app
def main():
    st.title("Plagiarism Detection with PDFs")

    # File uploader for PDF files
    pdf_file = st.file_uploader("Upload an original PDF file:", type=["pdf"])

    if pdf_file:
        st.subheader("Original PDF Content")
        original_text = extract_text_from_pdf(pdf_file)
        st.text_area("Original Text:", value=original_text, height=300)

        # Text input for new text
        st.subheader("Enter New Text to Check for Plagiarism")
        new_text = st.text_area("Enter new text:", height=200)

        # Button to perform plagiarism detection
        if st.button("Detect Plagiarism"):
            if new_text:
                # Preprocess the new text
                preprocessed_new_text = preprocess_text(new_text)
                preprocessed_original_text = preprocess_text(original_text)
                
                # Compare the new text with the original text
                similarity_ratio = similarity(preprocessed_new_text, preprocessed_original_text)
                st.write(f"Similarity Ratio: {similarity_ratio:.2%}")
                if similarity_ratio > 0.75:
                    st.error("Plagiarism detected!")
                else:
                    st.success("No plagiarism detected.")
            else:
                st.warning("Please enter new text to check for plagiarism.")

# Function to calculate text similarity using Jaccard similarity
def similarity(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity_ratio = intersection / union if union > 0 else 0
    return similarity_ratio

if __name__ == "__main__":
    main()
