from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader


def get_documents(file_name, chunk_size, chunk_overlap):
    if file_name.endswith(".txt"):
        loader = TextLoader(file_name)
    elif file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_name)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    docs = text_splitter.split_documents(documents)
    return docs


def get_context(documents, query, n_results, model_name):
    embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
    db = FAISS.from_documents(documents, embedding_function)
    docs = db.similarity_search(query, k=n_results)
    context = [document.page_content for document in docs]
    return '\n\n'.join(context)
