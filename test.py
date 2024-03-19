import os
import httpx
from langchain.chat_models import AzureChatOpenAI , ChatOpenAI
#from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.messages import HumanMessage
import openai

 

def init_llm(model="gpt-35-turbo-16k",
             deployment_name="gpt-35-16k",
             temperature=0,
             max_tokens=800,
             stop="<|im_end|>",
             ):
    llm = AzureChatOpenAI(deployment_name=deployment_name,
                      model=model,
                      temperature=temperature,
                      max_tokens=max_tokens,
                      model_kwargs={"stop": ["<|im_end|>"]})
    return llm
# azure_configs = {     
#     "azure_endpoint" : "https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/canadaeast/",
#     "openai_api_version" :"2023-05-15",
#     "azure_deployment" : "gpt-35",
#     "openai_api_key" :"5d57e861530c4f30b60dd25fae432f52",
#     "openai_api_type" :"azure"
#     # "http_client": httpx.Client(verify=False) #SSL Disabled
# }

# os.environ['OPENAI_API_BASE'] = 'https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/canadaeast/'
os.environ['OPENAI_API_BASE'] = 'https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/northcentralus'
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
    
openai.api_version ='2023-05-15'
openai.api_base = 'https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/northcentralus'
# llm = AzureChatOpenAI(**azure_configs)
llm = init_llm()
result = llm([HumanMessage(content='Tell me about pluto')])
print(result)