from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from chains.chatgpt import init_llm
import openai
from langchain.chains import RetrievalQA
class TMFRAG ():
    def initTMF(self, dbPath):
        self.llm=init_llm()
        self.embeddings = OpenAIEmbeddings(deployment_id="text-embedding-ada",model="text-embedding-ada-002",deployment="text-embedding-ada", chunk_size=1)
# load the vector store to memory
        self.vectorStore = FAISS.load_local(dbPath, self.embeddings)
        self.retriever = self.vectorStore.as_retriever(search_type="similarity", search_kwargs={
                                     "k": 5})  # returns 2 most similar vectors/documents
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=self.retriever, return_source_documents=True)
        
        
        
    def queryTMF(self,query):
        response = self.qa({"query": query})
        return response
