import streamlit as st
from enum import Enum
from dotenv import load_dotenv, find_dotenv
from chains.chatgpt import executeQuery
from chains.tmfRAG import TMFRAG

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
GPTtext = st.text_area()
TMFtext = st.text()
ThreeGPPText = st.text()
st.write(selectedStandard) 

if question and (selectedStandard == Standard.CHATGPT.value):
    GPTAnswer = executeQuery(question)
if question and (selectedStandard == Standard.TMF.value):
    TMFAnswer = mytmfRAG.queryTMF(question)
if question and (selectedStandard == Standard.THREEGPP.value):
    ThreeGPPAnswer = my3GPPRAG.queryTMF(question)
if GPTAnswer != None:
    st.title(body="GPT Answer")
    st.text(body= GPTAnswer['result'])    
if ThreeGPPAnswer != None:
    st.title(body="3GPP Answer")
    st.text(body= ThreeGPPAnswer['result'])    
if TMFAnswer != None:
    st.title(body="TMF Answer")
    st.text(body= TMFAnswer['result'])   