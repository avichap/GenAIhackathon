from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.word_document import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
def embedContent(contentType , uploadFile):
    embeddings = OpenAIEmbeddings(
        deployment="text-embedding-ada",
        #deployment="gpt-35-turbo-4k",
        model="text-embedding-ada-002",
        # model="gpt-35-turbo",
        openai_api_base="https://dev-mgmt-infra.amaiz.corp.amdocs.azr/v1/hackathon/regions/northcentralus",
        openai_api_type="azure",
        #_chunk_size=100,
        show_progress_bar=False)
    print (f' the embeddings actual chunk size: {embeddings.chunk_size}')
    dbLocation=None
    if contentType == "TMF":
        dbLocation = "./db/TMF/"
    elif contentType == "3GPP":
        dbLocation = "./db/3GPP/"
    db = FAISS.load_local(dbLocation, embeddings)
    fileName = os.path.basename(os.path.normpath(uploadFile.name))

    tempContentfile=f"./{fileName}"
    with open(tempContentfile, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(uploadFile.getbuffer())
    loader = None
    if (uploadFile.name.endswith('.pdf')):
        loader = PyPDFLoader(tempContentfile)
    elif (uploadFile.name.endswith('.docx')):
        loader = Docx2txtLoader(tempContentfile)
    pages = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100))
    pages_len=  len(pages)
    print(f'Number of pages of  :{pages_len}')
    db.add_documents(documents=pages)
    # save the FAISS index to disk
    db.save_local(dbLocation)