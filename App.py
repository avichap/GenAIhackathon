import streamlit as st
import os
from enum import Enum
from dotenv import load_dotenv, find_dotenv
from chains.chatgpt import executeQuery
from chains.tmfRAG import TMFRAG
from langchain.docstore.document import Document
from utils.contentUtil import embedContent
class Standard(Enum):
        TMF = 'TMF'
        THREEGPP = '3GPP'
        CHATGPT = 'CHATGPT' 


print('******Im in the begining of the code')
load_dotenv()
def AssitantPage():
    mytmfRAG = TMFRAG()
    my3GPPRAG = TMFRAG()
    mytmfRAG.initTMF(dbPath="C:/dev/hackathon/db/TMF/")
    my3GPPRAG.initTMF(dbPath="C:/dev/hackathon/db/3GPP/")
    
    # Streamlit UI elements
    GPTAnswer = None
    ThreeGPPAnswer= None
    TMFAnswer = None
    st.title("Telecom Standards Assistant")
    selectedStandard = st.selectbox(
                'Choose Standard',
                [source.value for source in Standard]
    )

    question = st.text_input(
        "Ask Somtehing...",
        placeholder="Please explain the standard or generate an artifact ",
        disabled=not selectedStandard
    )


    if question and (selectedStandard == Standard.CHATGPT.value):
        GPTAnswer = executeQuery(question)
    if question and (selectedStandard == Standard.TMF.value):
        TMFAnswer = mytmfRAG.queryTMF(question)
    if question and (selectedStandard == Standard.THREEGPP.value):
        ThreeGPPAnswer = my3GPPRAG.queryTMF(question)
        
    # print (f'GPTAnswer :{GPTAnswer}')
    # print (f'ThreeGPPAnswer :{ThreeGPPAnswer}')
    # print (f'TMFAnswer :{TMFAnswer}')

    if GPTAnswer != None:
        st.title(body="GPT Answer")
        st.text_area(label="GPT answer",value= GPTAnswer.content,height=400)    
    if ThreeGPPAnswer != None:
        st.title(body="3GPP Answer")
        st.text_area(label="3GPP answer",value= ThreeGPPAnswer['result'],height=400)
        documents = ThreeGPPAnswer['source_documents'];
        documentsSet = set()
        for document in documents:
            documentsSet.add(os.path.basename(document.metadata['source']))
        st.title(body="3GPP Source Documents")
        for document in documentsSet:
            st.text(document)
    if TMFAnswer != None:
        st.title(body="TMF Answer")
        st.text_area(label="TMF answer",value=TMFAnswer['result'],height=400)
        st.title(body="TMF Source Documents")
        documents = TMFAnswer['source_documents'];
        documentsSet = set()
        for document in documents:
            documentsSet.add(os.path.basename(document.metadata['source']))
        for document in documentsSet:
            st.text(document)
def uploadContent():
    
    selectedStandard = st.selectbox(
                'Choose Standard',
                [source.value for source in Standard])
    upload_file = st.file_uploader(label="Upload Content",type=['pdf','docx'])  
    
    if selectedStandard!=None and upload_file!=None:
        if selectedStandard == Standard.CHATGPT.value:
            st.write('CHATGPT does not allow embedding')
        else:
            embedContent(selectedStandard,upload_file)   
            st.write(f'Content has been embedded successfully to  database')

page_names_to_funcs = {
    # "—": intro,
    "Use Telecom Standards Assitant": AssitantPage,
    "Upload to knowledge base": uploadContent
}
demo_name = st.sidebar.selectbox("Choose an Option", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
    
    
     