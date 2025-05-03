import streamlit as st
import pandas as pd
from fpdf import FPDF
import uuid
import os

st.title("CSV to PDF Converter")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("CSV Preview:")
    st.dataframe(df)

    if st.button("Convert to PDF"):
        try:
            unique_id = str(uuid.uuid4())
            pdf_path = f"converted_{unique_id}.pdf"

            # Create PDF
            pdf = FPDF(orientation='L', unit='mm', format='A4')  # Landscape for wide tables
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Set column widths (adjustable)
            col_width = pdf.w / (len(df.columns) + 1)

            # Header
            pdf.set_fill_color(200, 220, 255)
            for col in df.columns:
                pdf.cell(col_width, 10, str(col), border=1, fill=True)
            pdf.ln()

            # Rows
            for i, row in df.iterrows():
                for item in row:
                    text = str(item)
                    # Truncate long values
                    if len(text) > 30:
                        text = text[:27] + "..."
                    pdf.cell(col_width, 10, text, border=1)
                pdf.ln()

            pdf.output(pdf_path)

            st.success("PDF generated successfully!")

            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="your_data.pdf")

            os.remove(pdf_path)

        except Exception as e:
            st.error(f"Error: {e}")
