import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Show title and description.
st.title("📄 PDF Splitter")
st.write(
    "Upload a PDF document, and this app will split it at the 'Judge's Instructions' section. "
    "You'll get two downloadable PDFs: one with content before and another with content from the Judge's Instructions onward."
)

# Allow users to upload multiple PDF files.
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# Function to split PDF at "Judge's Instructions"
def split_pdf(file):
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    before_instructions = PdfWriter()
    after_instructions = PdfWriter()
    
    found_instructions = False
    
    # Loop through each page and split based on keyword
    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        
        if "JUDGE INSTRUCTIONS" in text and not found_instructions:
            found_instructions = True
        
        # Add pages to respective PDF writer
        if found_instructions:
            after_instructions.add_page(page)
        else:
            before_instructions.add_page(page)
    
    # Save the split PDFs to BytesIO objects
    before_output = BytesIO()
    after_output = BytesIO()
    before_instructions.write(before_output)
    after_instructions.write(after_output)
    
    # Prepare BytesIO objects for download
    before_output.seek(0)
    after_output.seek(0)
    
    return before_output, after_output

# Process each uploaded file
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name.rsplit(".", 1)[0]  # Get filename without extension
        
        # Split the PDF
        before_pdf, after_pdf = split_pdf(uploaded_file)
        
        # Create download buttons for each split PDF
        st.download_button(
            label=f"Download {file_name}-comp.pdf",
            data=before_pdf,
            file_name=f"{file_name}-comp.pdf",
            mime="application/pdf"
        )
        
        st.download_button(
            label=f"Download {file_name}-judge.pdf",
            data=after_pdf,
            file_name=f"{file_name}-judge.pdf",
            mime="application/pdf"
        )
