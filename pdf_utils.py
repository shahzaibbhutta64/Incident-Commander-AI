import pypdf

def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts text content from an uploaded PDF file."""
    try:
        reader = pypdf.PdfReader(uploaded_file)
        extracted_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(f"--- PAGE {i+1} ---\n{text}")
        return "\n\n".join(extracted_text)
    except Exception as e:
        return f"Error extracting PDF text from {uploaded_file.name}: {str(e)}"
