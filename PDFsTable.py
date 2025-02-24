import streamlit as st
import tabula
import os
from io import BytesIO
import pandas as pd

def convert_pdf_to_csv(pdf_file, method):
    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.getbuffer())
    
    # Determine extraction method
    lattice = method == "Lattice"
    stream = method == "Stream"
    
    # Convert PDF to CSV
    output_csv = "output.csv"
    tabula.convert_into("temp.pdf", output_csv, output_format='csv', lattice=lattice, stream=stream, pages='all')
    
    # Read and return the CSV file
    df = pd.read_csv(output_csv)
    return df

st.title("PDF Table to CSV Converter")

st.write("Upload a PDF containing tables, select the extraction method, and get the CSV output.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
method = st.selectbox("Select Extraction Method", ["Lattice", "Stream", "Guess"], index=0)

if uploaded_file is not None:
    if st.button("Convert to CSV"):
        df = convert_pdf_to_csv(uploaded_file, method)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="converted_table.csv", mime="text/csv")
        st.dataframe(df)
