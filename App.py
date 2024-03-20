import streamlit as st
import os
from enum import Enum
from dotenv import load_dotenv, find_dotenv
from chains.chatgpt import executeQuery
from chains.tmfRAG import TMFRAG
from langchain.docstore.document import Document

print('******Im in the begining of the code')
load_dotenv()
mytmfRAG = TMFRAG()
my3GPPRAG = TMFRAG()
mytmfRAG.initTMF(dbPath="C:/dev/hackathon/db/TMF/")
my3GPPRAG.initTMF(dbPath="C:/dev/hackathon/db/3GPP/")
class Standard(Enum):
    TMF = 'TMF'
    THREEGPP = '3GPP'
    CHATGPT = 'CHATGPT'
with st.sidebar:
    st.markdown(
        "Please select the standard you want to use \n"
        "1. TMF \n"
        "2. 3GPP \n"
        "3. use CHATGPT\n"
    )   
# Streamlit UI elements
GPTAnswer = None
ThreeGPPAnswer= None
TMFAnswer = None
st.title("Telco Standard Guru")
selectedStandard = st.selectbox(
            'Choose Standard',
            [source.value for source in Standard]
)

question = st.text_input(
    "Ask Somthing Our Standard guru",
    placeholder="How should I create an TMF intent",
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
    
    
     