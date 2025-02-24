import streamlit as st
import tabula
import os
from io import BytesIO
import pandas as pd

def convert_pdf_to_csv(pdf_file, method, filename):
    # Save uploaded file temporarily
    with open(filename, "wb") as f:
        f.write(pdf_file.getbuffer())
    
    # Determine extraction method
    lattice = method == "Lattice"
    stream = method == "Stream"
    
    # Convert PDF to CSV
    output_csv = f"{filename}.csv"
    tabula.convert_into(filename, output_csv, output_format='csv', lattice=lattice, stream=stream, pages='all')
    
    # Read and return the CSV file
    df = pd.read_csv(output_csv)
    return df, output_csv

st.title("PDF Table to CSV Converter")

st.write("Upload PDFs containing tables, select the extraction method, and get the CSV outputs.")

method_description = st.markdown(
    """
    **Data Extraction Methods:**  
    - **Lattice:** Works best for tables with clearly defined borders and grid lines.  
    - **Stream:** Works best for tables without visible borders or irregular column alignments.  
    - **Guess:** Automatically selects the best method for table extraction.
    """
)

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
method = st.selectbox("Select Extraction Method", ["Lattice", "Stream", "Guess"], index=0)

if uploaded_files:
    for uploaded_file in uploaded_files:
        df, output_csv = convert_pdf_to_csv(uploaded_file, method, uploaded_file.name)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(f"Download {uploaded_file.name}.csv", data=csv, file_name=output_csv, mime="text/csv")
        st.dataframe(df)
