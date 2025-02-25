# AccuTable: PDF to CSV (Batch Mode) using Tabula python library

## 🚀 Overview
AccuTable is a **Streamlit-based web application** that extracts tables from **text-based PDFs** and converts them into **CSV** files in batch mode. Users can choose an appropriate extraction method (**Lattice, Stream, or Guess**) for better accuracy.

## 🛠 Features
- **Batch Processing**: Upload multiple PDFs and convert them in one go.
- **Multiple Extraction Modes**: Supports **Lattice**, **Stream**, and **Guess** methods for extracting tables.
- **Automated ZIP Download**: Converted CSV files are packaged into a ZIP for easy download.
- **Interactive UI**: User-friendly interface built with **Streamlit**.

## 📦 Installation
To run this application locally, follow these steps:

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/streamlit-pdf-to-csv.git
cd streamlit-pdf-to-csv
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

## 🚀 Running the App
```sh
streamlit run app.py
```
This will open the Streamlit app in your browser.

## 🔄 Usage Guide
1. **Upload PDFs**: Click on the **"Upload PDF files"** button and select multiple PDF files.
2. **Choose Extraction Method**:
   - **Lattice**: Best for tables with grid lines.
   - **Stream**: Best for tables without visible borders.
   - **Guess**: Automatically selects the best method.
3. **Convert to CSV**: Click **"Convert to CSV"** and wait for the process to complete.
4. **Download the ZIP**: Once conversion is done, click **"Download All as ZIP"** to get all CSV files.

## 🔧 Dependencies
- **Python 3.8+**
- **Streamlit**
- **Tabula-py** (Requires Java installed)
- **Pandas**

Install dependencies using:
```sh
pip install streamlit tabula-py pandas
```

## 📌 Notes
- **Only works with text-based PDFs** (scanned PDFs are not supported).
- **Requires Java** for `tabula-py` to work.
- Temporary files are cleaned up automatically after conversion.



