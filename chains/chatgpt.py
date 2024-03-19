from langchain.chat_models import AzureChatOpenAI
import openai
import os
import streamlit as st
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage

def init_llm(model="gpt-35-turbo-16k",
             deployment_name="gpt-35-16k",
             temperature=0,
             max_tokens=800,
             stop="<|im_end|>",
             ):
    openai.api_type = "azure"
    os.environ['OPENAI_API_BASE'] = 'https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/northcentralus'
    os.environ['OPENAI_API_VERSION'] = '2023-05-15'
    openai.api_version ='2023-05-15'
    openai.api_base = 'https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/northcentralus'
    openai.api_key = "5d57e861530c4f30b60dd25fae432f52"
    llm = AzureChatOpenAI(deployment_name=deployment_name,
                      model=model,
                      temperature=temperature,
                      max_tokens=max_tokens,
                      model_kwargs={"stop": ["<|im_end|>"]})
    return llm
def executeQuery(query):
    llm = init_llm()
    # openai.api_version = os.environ["OPENAI_API_VERSION"]
    # openai.api_base = os.environ["AZURE_OPENAI_ENDPOINT"]
    # openai.api_key = os.environ["AZURE_OPENAI_KEY"]
    humanMessage = HumanMessage(content=query)
    
    systemMessage = SystemMessage(content="You are a HELPFUL assistant knowledged in Telco standards answering users questions. Answer in a clear and concise manner.")
    messages = [systemMessage,humanMessage]
    answer = llm(messages)
    return answer