__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader


MODEL_NAME = 'distiluse-base-multilingual-cased-v1'

def get_context(file_name, query, chunk_size, chunk_overlap, n_results):
    loader = TextLoader(file_name, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function = len)
    docs = text_splitter.split_documents(documents)

    embedding_function = SentenceTransformerEmbeddings(model_name=MODEL_NAME)

    db = Chroma.from_documents(docs, embedding_function)

    docs = db.similarity_search(query, k=n_results)

    result = []
    for document in docs:
        result.append(document.page_content)

    return "\n".join(result)


if __name__ == "__main__":
    query = "Wie viel Einwohner hat Israel?"
    context = get_context("test.txt", query, chunk_size=250, chunk_overlap=0, n_results=3)
    
    print(context)


