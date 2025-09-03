from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document


# Extract Data from PDF
def load_pdf(data):
    loader = DirectoryLoader(data,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

# Filter Document
def filter_documents(documents: List[Document]) -> List[Document]:
    filtered_docs: List[Document] = []
    for doc in documents:
        src = doc.metadata.get('source')
        filtered_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={'source': src}
            )
        )
    return filtered_docs

# Splitting Document (Chuncking)
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

# Download Embedding Model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings
