import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

st.markdown(
"""
<style>
.stApp{
    background-color: #000000;
    color: #f0f0f5;
    align-items: center;
    justify-content: center;
    }
</style>
""",
unsafe_allow_html=True
)

#title and description
st.title("📀Data Sweeper By Tooba Saleem")
st.write("This is a simple web app that allows you to upload a dataset and perform some basic data cleaning operations on it. The app will display the first 5 rows of the dataset and allow you to download the cleaned dataset.")

#uploading the dataset
uploaded_files = st.file_uploader("Upload a dataset", type=["cvs", "xlsx"], accept_multiple_files=(True))
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        #file details
        st.write("🔍 Preview the head of the Dataframe:")
        st.dataframe(df.head())

        #cleaning the dataset
        st.subheader("❌Data Cleaning")
        if st.checkbox(f"Clean data for {file.name}"):
            col1,col2 =st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from the file :{file.name}" ):
                    df.drop_duplicates(inplace=True)
                    st.write("Removed duplicates!")
            with col2:
                if st.button(f"Fill missing values from the file :{file.name}" ):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Filled missing values!")
        st.subheader("Select the columns to Keep")
        columns = st.multiselect("Select the columns to keep:{file.name}", df.columns, default=df.columns)
        df = df[columns]


        #data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for the file:{file.name}"):
            st.bar_chart(df.select_dtypes(include=['number'].iloc[:,:2]))
        
        #conversion options:
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert the file:{file.name} to", ["CVS", "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Click here to download the {file.name} as {conversion_type} file",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 All operations completed successfully!")
