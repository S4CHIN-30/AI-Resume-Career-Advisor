import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DATA_PATH = "data/job_descriptions"
VECTORSTORE_PATH = "vectorstore/job_descriptions"


def create_vectorstore():

    print("Loading Job Description PDFs...")

    loader = PyPDFDirectoryLoader(DATA_PATH)

    documents = loader.load()

    print(f"Loaded {len(documents)} pages.")

    print("Splitting documents...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating FAISS vector database...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    os.makedirs(VECTORSTORE_PATH, exist_ok=True)

    vectorstore.save_local(
        VECTORSTORE_PATH
    )

    print("Vector database created successfully!")

    return vectorstore


def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def search_jobs(query, k=3):

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    vectorstore = create_vectorstore()

    query = """
    Python developer with Python, SQL, REST APIs,
    Git, backend development and Django or Flask skills.
    """

    results = vectorstore.similarity_search(
        query,
        k=3
    )

    print("\n================================")
    print("       RAG SEARCH RESULTS")
    print("================================")

    for i, document in enumerate(results, start=1):

        print(f"\nRESULT {i}")
        print("--------------------------------")

        print("Source:")
        print(document.metadata.get("source"))

        print("\nContent:")
        print(document.page_content[:500])