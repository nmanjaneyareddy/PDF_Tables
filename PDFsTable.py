import streamlit as st
import tabula
import os
import zipfile
from io import BytesIO
from tempfile import NamedTemporaryFile

# PDF and Table Icons
pdf_icon = "https://cdn.pixabay.com/photo/2020/03/10/17/02/pdf-4919559_1280.png"
table_icon = "https://img.freepik.com/premium-psd/csv-file_689261-99.jpg"

# Display icons and title
col1, col2, col3 = st.columns([1, 0.5, 1])

with col1:
    st.image(pdf_icon, width=50)

with col2:
    st.markdown("<h4 style='text-align: center;'>➡️</h4>", unsafe_allow_html=True)

with col3:
    st.image(table_icon, width=50)

# Streamlit App Title
st.title("AccuTable: PDF to CSV)")

st.write(
    "🚀 This application extracts tables from **text-based PDFs only** and converts them into **CSV** files in batch mode. "
    "Users can choose the appropriate extraction method **(Lattice, Stream, or Guess)** for accurate table recognition 🚀"
)

# File uploader for multiple PDFs
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Extraction method selection
st.markdown("""
**Data Extraction Methods:**  
- **Lattice:** Best for tables with grid lines.  
- **Stream:** Best for tables without visible borders.  
- **Guess:** Automatically selects the best method.
""")

# Select the method of extraction
method = st.selectbox("Select Extraction Method", ["Lattice", "Stream", "Guess"], index=0)

# Function to convert PDFs to CSV without reading tables
def batch_convert_pdfs(pdf_files, method):
    converted_files = []

    for pdf_file in pdf_files:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_file.getbuffer())
            temp_pdf_path = temp_pdf.name  # Get temporary PDF path

        # Define CSV output path
        output_csv = temp_pdf_path.replace(".pdf", ".csv")

        # Determine extraction mode
        lattice = method == "Lattice"
        stream = method == "Stream"
        
        if method == "Guess":  # If Guess, let tabula decide the best mode
            lattice, stream = None, None

        try:
            tabula.convert_into(temp_pdf_path, output_csv, output_format='csv', lattice=lattice, stream=stream, pages='all')
            converted_files.append(output_csv)
        except Exception as e:
            st.error(f"Error converting {pdf_file.name}: {e}")
        
        # Remove the temporary PDF file after conversion
        os.remove(temp_pdf_path)

    return converted_files

# Function to create a ZIP file
def create_zip(files):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
            os.remove(file)  # Clean up CSV file after adding to ZIP
    zip_buffer.seek(0)
    return zip_buffer

# Process and download ZIP
if uploaded_files and st.button("Convert to CSV"):
    converted_files = batch_convert_pdfs(uploaded_files, method)

    if converted_files:
        st.success(f"✅ Successfully converted {len(converted_files)} file(s)!")

        # Create ZIP file
        zip_file = create_zip(converted_files)

        # Provide ZIP download
        st.download_button(
            label="📥 Download All as ZIP",
            data=zip_file,
            file_name="Converted_CSVs.zip",
            mime="application/zip"
        )

        st.balloons()  # 🎈 Success animation
