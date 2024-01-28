#pip install streamlit -q
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

import pandas as pd

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function load gemini model

def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt, question])
    return response.text


prompt = '''
You are an expert in converting English questions to SQL query!
    Data is {df} and The SQL database has the following columns - {columns} \n\n
    User can ask any questions from the database. Like tell me top 5 entries from the particular column,
    also the sql code should not have ``` in beginning or end and sql word in output
    Please do not make things up, Answer accurately with respect to database only
    While giving answers, go in the dataset and check and then write column names accordingly
    Don't make up column names, select appropriate column from the dataset columns only.

'''

## Streamlit App

def main():
    st.set_page_config("SQL Query Generator")
    st.header("Generate Your SQL Query Here💁")

    question = st.text_area("Ask a Question about the dataset")

   
    a = st.button('Submit')

    if a:
        response = get_gemini_response(question, prompt)
        st.subheader("The SQL for given questions is")
        st.write(response)

    with st.sidebar:
            st.title("Menu:")
            pdf_docs = st.file_uploader("Upload your Data File and Click on the Submit & Process Button", accept_multiple_files=False)
            if st.button("Submit & Process"):
                    with st.spinner("Processing..."):
                        df = pd.read_csv(pdf_docs)
                        columns = df.columns
                        st.success("Done")

if __name__ == "__main__":
    main()
