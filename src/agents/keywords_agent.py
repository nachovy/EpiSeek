import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def extract_keywords(question, model_name='gpt-4o-mini'):
    """
    Extract keywords from a research question using an LLM.
    Args:
        question (str): The research question.
        model_name (str): The name of the LLM model to use.
    Returns:
        list: A list of extracted keywords.
    """
    prompt = PromptTemplate(
        input_variables=["question"],
        template=(
            "You are an AI assistant specialized in extracting key concepts from research questions. "
            "Extract 5 most relevant keywords from the following question and return them as a comma-separated list:\n\n"
            "Question: {question}\n"
            "Keywords:"
        )
    )

    llm = ChatOpenAI(model=model_name, temperature=0)
    chain = prompt | llm
    keywords_str = chain.invoke({"question": question}, config={"configurable": {"session_id": "user1"}}).content
    if isinstance(keywords_str, str):
        keywords = [keyword.strip() for keyword in re.split(r",\s*", keywords_str) if keyword]
    else:
        keywords = []

    return keywords
