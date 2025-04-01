import os
import re
import requests

SAVE_DIR = "downloaded_papers"
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(filename):
    """
    Remove invalid characters from a filename.
    Args:
        filename (str): The original filename.
    Returns:
        str: The sanitized filename.
    """
    invalid_chars = r'[\\/*?:"<>|]'
    return re.sub(invalid_chars, '', filename)

def download_semantic_scholar(paper):
    """Download a paper from Semantic Scholar.
    Args:
        paper (dict): Dictionary containing paper details.
    Returns:
        str: The path to the downloaded PDF file.
    """
    pdf_url = paper.get("pdf_url", None)
    title = sanitize_filename(paper.get("title", 'untitled'))
    file_path = os.path.join(SAVE_DIR, f"{title}.pdf")
    if os.path.exists(file_path):
        print(f"Paper already downloaded: {file_path}")
        return file_path
    response = requests.get(pdf_url)
    if response.status_code == 200:
        try:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Paper downloaded: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error downloading paper: {e}")
    return None

def download_papers(paper):
    """Download paper from Semantic Scholar.
    Args:
        paper (dict): Dictionary containing paper details.
    Returns:
        str: The path to the downloaded PDF file.
    """
    pdf_url = paper.get("pdf_url", None)
    title = paper.get("title", None)
    if pdf_url:
        return download_semantic_scholar(paper)
    else:
        print("Cannot download paper:", title)
        return None