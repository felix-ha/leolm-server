from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
import wikipedia
wikipedia.set_lang("de")
import tempfile
from pathlib import Path


MODEL_NAME = 'distiluse-base-multilingual-cased-v1'


def get_documents(file_name, chunk_size, chunk_overlap): 
    loader = TextLoader(file_name, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function = len)
    docs = text_splitter.split_documents(documents)

    return docs


def get_context(documents, query, n_results):
    embedding_function = SentenceTransformerEmbeddings(model_name=MODEL_NAME)

    db = FAISS.from_documents(documents, embedding_function)

    docs = db.similarity_search(query, k=n_results)

    result = []
    for document in docs:
        result.append(document.page_content)

    return result


def get_wiki_article(keyword):
    result = wikipedia.search(keyword)
    article = wikipedia.page(result[0])
    return article  


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        path_to_upload = tmpdir_path / "tmp.txt"
        
        wiki_keyword = "Vertrag von Versailles (1756)"
        wiki_article = get_wiki_article(wiki_keyword)

        with open(path_to_upload, "w", encoding="utf-8") as f:
            f.write(wiki_article.content)          

        documents = get_documents(path_to_upload, chunk_size=500, chunk_overlap=25)

        for i, document in enumerate(documents):
            print(f'{i} {len(document.page_content)} {document}\n\n')

        query = "Wann fand das geheime Treffen statt?"
        context = get_context(documents, query,  n_results=5)

        print("----------context----------")
        for i, c in enumerate(context):
            print(f'{i} {c}\n\n')
