import os
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

session_histories = {}

def get_session_history(session_id: str):
    """Retrieve the session history for a given session ID.
    Args:
        session_id (str): The ID of the session.
    Returns:
        list: A list of message history objects.
    """
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]

def read_pdf(pdf_path):
    """Read the content of a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: The text content of the PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip() if text else None
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

def chunk_text(text, max_tokens=4096):
    """Split text into chunks based on token limit.
    Args:
        text (str): The text to chunk.
        max_tokens (int): Maximum number of tokens per chunk.
    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    for i in range(0, len(text), max_tokens):
        chunks.append(text[i:i + max_tokens])
    return chunks

def answer_question(papers, question, session_id, model_name='gpt-4o-mini', follow_up=False):
    """Answer a question using the vector store.
    Args:
        papers (List[Dict]): List of papers, each containing 'title', 'abstract', and optionally 'content'.
        question (str): The question to answer.
        session_id (str): The ID of the session.
        model_name (str): The name of the LLM model to use.
        follow_up (bool): Whether the question is a follow-up question.
    Returns:
        str: The answer to the question.
    """
    llm = ChatOpenAI(model=model_name, temperature=0)
    prompt = PromptTemplate.from_template(
        "You are an expert research assistant. You will receive multiple sections of academic papers. "
        "Do not generate an answer yet. Read and understand the context carefully. "
        "Do not make up an answer if you cannot get the information to answer this question from the papers. \n\n"
        "User: {input}\n"
        "Assistant:"
    )
    conversation_chain = RunnableWithMessageHistory(
        llm,
        get_session_history=get_session_history,
        input_template=prompt
    )
    if not follow_up:
        if papers is None or not papers:
            return "No relevant papers found."
        # Build the context from the papers
        context_list = []
        for paper in papers:
            title = paper.get("title", "")
            year = paper.get("year", "")
            authors = ", ".join(paper.get("authors", []))
            abstract = paper.get("abstract", "")

            pdf_path = paper.get("pdf_path")
            paper_text = read_pdf(pdf_path) if pdf_path and os.path.exists(pdf_path) else abstract # Use abstract if no PDF content is available
            # Chunk the text if it exceeds the token limit
            if paper_text:
                content_chunks = chunk_text(paper_text)
                for chunk in content_chunks:
                    context_list.append(
                        f"Title: {title}\n"
                        f"Year: {year}\n"
                        f"Authors: {authors}\n"
                        f"Content: {chunk}"
                    )
        # Pass the context to the LLM
        full_context = "\n".join(context_list) if context_list else "No relevant papers found."
        question_prompt = f"{full_context}\nBased on everything you've read, answer the following question concisely.: {question}"
    else:
        # Only pass the question to the LLM if it is a follow-up
        question_prompt = f"Based on the previous conversation, answer the following question concisely: {question}"
    
    response = conversation_chain.invoke(
        {"input": question_prompt},
        config={"configurable": {"session_id": session_id}}
    )
    
    return response.content
