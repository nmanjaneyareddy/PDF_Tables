import base64
import streamlit as st
import tabula
import os

# PDF and Table Icons
pdf_icon = "https://cdn.pixabay.com/photo/2020/03/10/17/02/pdf-4919559_1280.png"
table_icon = "https://img.freepik.com/premium-psd/csv-file_689261-99.jpg"

# Display icons and title
col1, col2, col3 = st.columns([1, 0.5, 1])

with col1:
    st.image(pdf_icon, width=50)

with col2:
    st.markdown("<h4>  ---------></h4>", unsafe_allow_html=True)

with col3:
    st.image(table_icon, width=50)

# Streamlit App Title
st.title("AccuTable: PDF to CSV (Batch Mode)")

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
    lattice = method == "Lattice"
    stream = method == "Stream"

    converted_files = []

    for pdf_file in pdf_files:
        filename = pdf_file.name
        output_csv = f"{filename}.csv"

        # Save file temporarily
        with open(filename, "wb") as f:
            f.write(pdf_file.getbuffer())

        # Convert PDF to CSV (Batch Mode)
        try:
            tabula.convert_into(filename, output_csv, output_format='csv', lattice=lattice, stream=stream, pages='all')
            converted_files.append(output_csv)
        except Exception as e:
            st.error(f"Error converting {filename}: {e}")

    return converted_files

# Process and download CSVs
if uploaded_files and st.button("Convert to CSV"):
    converted_files = batch_convert_pdfs(uploaded_files, method)

    for csv_filename in converted_files:
        with open(csv_filename, "rb") as f:
            csv_data = f.read()  # Read as bytes
            b64 = base64.b64encode(csv_data).decode()  # Encode to Base64
            href = f'<a href="data:file/csv;base64,{b64}" download="{csv_filename}">Click here to download {csv_filename}</a>'
            st.markdown(href, unsafe_allow_html=True)  # Auto-download trigger
