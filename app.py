import streamlit as st
import pandas as pd
from emotion_analysis import get_emotion
import base64


def read_data(file_path):
    file_extension = file_path.split('.')[-1].lower()
    
    if file_extension == 'xlsx' or file_extension == 'xls':
        data = pd.read_excel(file_path)
    elif file_extension == 'csv':
        data = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Only Excel (xlsx, xls) and CSV (csv) files are supported.")
    
    return data


# Streamlit app
def main():
    st.title("Text Emotion Detection")
    menu = ["Input Text", "Batch Processing"]
    option = st.sidebar.radio("Select an option", menu)


    if option == "Input Text":
        text = st.text_area("Enter your text:")
        if st.button("Submit"):
            if text.strip() != "":
                emotion_detail, confidence_score = get_emotion(text)
                st.write("Detected Emotion")
                st.write(f"{emotion_detail[0]} - {confidence_score}")
            else:
                st.write("Please enter some text.")

    elif option == "Batch Processing":
        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_extension = file_name.split('.')[-1].lower()
            file_name = uploaded_file.name
            if file_extension == 'xlsx' or file_extension == 'xls':
                dataframe = pd.read_excel(uploaded_file)
            elif file_extension == 'csv':
                dataframe = pd.read_csv(uploaded_file)
            else:
                raise ValueError("Unsupported file format. Only Excel (xlsx, xls) and CSV (csv) files are supported.")
            # dataframe = pd.read_excel(uploaded_file)
            if "text" not in dataframe.columns:
                st.write("CSV file should have a 'text' column.")
            else:
                dataframe["emotion"], dataframe["confidence"] = zip(*dataframe["text"].map(get_emotion))
                st.write("Detected Emotions")
                st.write(dataframe)
                # Download button
                csv = dataframe.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to CSV string
                href = f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv">Download</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            pass

if __name__ == '__main__':
    main()
