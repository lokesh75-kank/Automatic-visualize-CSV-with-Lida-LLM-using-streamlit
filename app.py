#create GUI
import streamlit as st
from lida import Manager, TextGenerationConfig, llm
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def base64_to_image(base64_string):

    #Decode the base64 string
    byte_data = base64.b64decode(base64_string)

    #uses BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

lida = Manager(text_gen=llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5 , model = "gpt-3.5-turbo-0301" , use_cache=True)

menu = st.sidebar.selectbox("choose an option", ["Summarize","Question based Graph"])

if menu == "Summarize":
    st.subheader("Summarization of your data")
    file_uploader = st.file_uploader("Upload your file here", type= ["csv","xlsx"])
    if file_uploader is not None:
        path_to_save = "filename.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        #lets summarize our data
        summary = lida.summarize("filename.csv", summary_method="default", textgen_config=textgen_config)
        st.write(summary)

        #let get goals
        goals = lida.goals(summary, n = 2, textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)
        
        #lets visualze our data
        i = 0
        library = "seaborn"
        textgen_config = TextGenerationConfig(n=1, temperature= 0.5, use_cache=True)
        charts = lida.visualize(summary=summary, goal= goals[i], textgen_config=textgen_config, library=library)
        image_base64_string = charts[0].raster
        img = base64_to_image(image_base64_string)
        st.image(img)

elif menu == "Question based Graph":

    st.subheader("Visualize your data")
    file_uploader = st.file_uploader("Upload your file here", type= ["csv","xlsx"])
    if file_uploader is not None:
        path_to_save = "filename1.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())

        text_area = st.text_area("Write a prompt to generate a graph", height= 200)
        print("text_area",text_area)

        if st.button("Generate graph"):

            if len(text_area) > 0:

                st.info("Your query:" + text_area)

                lida = Manager(text_gen=llm("openai"))

                textgen_config = TextGenerationConfig(n=1, temperature= 0.5, use_cache=True)

                summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)

                user_query = text_area

                charts = lida.visualize(summary=summary, goal = user_query, textgen_config=textgen_config)

                imagebase64 = charts[0].raster

                img = base64_to_image(imagebase64)
                
                st.image(img)
# def main():
#     st.set_page_config(page_title="Demand Management knowledge base", page_icon=":books:")

#     st.header("Demand Management knowledge base:books")
#     st.text_input("Ask me a question")

#     with st.sidebar:
#         st.subheader("your Documents")
#         st.file_uploader("upload your pdfs here and click on 'process'")
#         st.button("Process")


# if __name__ == '__main__':
#     main()