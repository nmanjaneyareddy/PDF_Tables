import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

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

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)


st.markdown("""
**Data Extraction Methods:**  
- **Lattice:** Best for tables with grid lines.  
- **Stream:** Best for tables without visible borders.  
- **Guess:** Automatically selects the best method.
""")

st.markdown()
method = st.selectbox("**Select Extraction Method**", ["Lattice", "Stream", "Guess"], index=0)



if uploaded_files and st.button("Convert to CSV"):
    converted_files = convert_pdfs(uploaded_files, method)

    for filename, csv_data, df in converted_files:
        st.download_button(f"Download {filename}", data=csv_data, file_name=filename, mime="text/csv")
        st.dataframe(df)
