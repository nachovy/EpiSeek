from agents.keywords_agent import extract_keywords
from agents.search_agent import search_papers
from agents.download_agent import download_papers
from agents.qa_agent import answer_question

session_counter = 0
keywords = []
papers = []
answer = ""

def run_pipeline(question, top_k=5, follow_up=False):
    """
    Run the research pipeline.

    Args:
        question (str): The research question.
        top_k (int): Number of papers to return.
        follow_up (bool): Whether the question is a follow-up question.
    Returns:
        dict: A dictionary containing keywords, papers, and the answer to the question.
    """
    global session_counter
    global keywords
    global papers
    global answer
    if not follow_up:
        keywords = extract_keywords(question, model_name='gpt-4o-mini')
        papers = search_papers(' '.join(keywords), top_k=top_k)
        for paper in papers:
            paper['pdf_path'] = download_papers(paper)
        session_counter += 1  # Increment session counter for each new session
    answer = answer_question(
        papers=papers,
        question=question,
        session_id=str(session_counter),
        model_name='gpt-4o-mini',
        follow_up=follow_up
    )
    return {"keywords": keywords, "papers": papers, "answer": answer}
