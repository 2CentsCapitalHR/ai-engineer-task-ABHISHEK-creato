import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI

load_dotenv()

class RAGHandler:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorstore = None
        self.qa_chain = None
        
    def initialize_vectorstore(self, docs_path):
        if os.path.isdir(docs_path):
            loader = DirectoryLoader(docs_path, glob="data/adgm_documents.txt", loader_cls=TextLoader)
        elif os.path.isfile(docs_path):
            loader = TextLoader(docs_path)
        else:
            raise ValueError(f"Invalid path: {docs_path}")

        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        
    def initialize_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever()
        )
    
    def query(self, question: str) -> str:
        if not self.qa_chain:
            raise ValueError("QA chain not initialized")
        return self.qa_chain.run(question)
