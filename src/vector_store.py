from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

def create_vector_store(papers):
    """Create a FAISS vector store from a list of papers.

    Args:
        papers (List[Dict]): List of papers, each containing 'title' and 'abstract'.

    """
    embeddings = OpenAIEmbeddings()
    context = [
        f"Title: {paper['title']}\n"
        f"Abstract: {paper['abstract']}"
        for paper in papers
    ]
    vector_store = FAISS.from_texts(context, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_vector_store():
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local("faiss_index", embeddings)
    return vector_store
