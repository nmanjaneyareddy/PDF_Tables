import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

# Function to convert PDFs to CSV
def convert_pdfs(pdf_files, method):
    converted_files = []
    lattice = method == "Lattice"
    stream = method == "Stream"

    for pdf_file in pdf_files:
        filename = pdf_file.name
        output_csv = f"{filename}.csv"

        # Save file temporarily
        with open(filename, "wb") as f:
            f.write(pdf_file.getbuffer())

        # Convert PDF to CSV
        dfs = tabula.read_pdf(filename, pages="all", multiple_tables=True, lattice=lattice, stream=stream)
        
        # Merge tables if multiple tables are found
        if dfs:
            df = pd.concat(dfs)
        else:
            df = pd.DataFrame()

        # Convert dataframe to CSV
        csv = df.to_csv(index=False).encode("utf-8")
        converted_files.append((output_csv, csv, df))

    return converted_files

# Streamlit UI
st.title("PDF Table to CSV Converter")

st.markdown("""
**Data Extraction Methods:**  
- **Lattice:** Best for tables with grid lines.  
- **Stream:** Best for tables without visible borders.  
- **Guess:** Automatically selects the best method.
""")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
method = st.selectbox("Select Extraction Method", ["Lattice", "Stream", "Guess"], index=0)

if uploaded_files and st.button("Convert to CSV"):
    converted_files = convert_pdfs(uploaded_files, method)

    for filename, csv_data, df in converted_files:
        st.download_button(f"Download {filename}", data=csv_data, file_name=filename, mime="text/csv")
        st.dataframe(df)
