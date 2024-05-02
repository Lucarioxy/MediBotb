from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_DB_API')
os.environ['PINECONE_API_KEY']=PINECONE_API_KEY
pc=Pinecone(api_key=os.environ['PINECONE_API_KEY'], environment="us-west1-gcp")

def context_vector_db(context:str,user_id:str):
    try:
        if user_id not in pc.list_indexes().names():
            pc.create_index(
                name=user_id,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
            text=text_splitter.split_text(context)
            docs=text_splitter.create_documents(text)
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=user_id)
            return docsearch
        else:
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=512,chunk_overlap=50)
            text=text_splitter.split_text(context)
            docs=text_splitter.create_documents(text)
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            docsearch = PineconeVectorStore(index_name=user_id, embedding=embeddings)
            docsearch.add_texts(text)
            return docsearch
    except Exception as e:
        print(str(e))




