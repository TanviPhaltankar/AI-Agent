from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
import os

def init_memory():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    if not os.path.exists("data/vector_store"):
        os.makedirs("data/vector_store")

    store_path = "data/vector_store/index.faiss"

    if os.path.exists(store_path):
        return FAISS.load_local("data/vector_store", embeddings)
    else:
        return FAISS.from_texts(["User initial memory"], embeddings)

def save_memory(store):
    store.save_local("data/vector_store")
