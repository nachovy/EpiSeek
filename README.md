## EpiSeek
### Description
A literature search agent system for scientific questions based on Uvicorn + Vue 3, incorporating [LangChain](https://github.com/langchain-ai/langchain).
- Accept text questions
- Fetch relevant scientific papers
- Provide answer
- Interactive follow-up
### Usage
#### Set up environment:
```
git clone git@github.com:nachovy/EpiSeek.git
cd EpiSeek
pip install -r requirements.txt
export PYTHONPATH="src"
export OPENAI_API_KEY="your_openai_api_key"
```

#### Run backend:
```
uvicorn src.app:app --reload
```
or
```
python -m uvicorn src.app:app --reload
```

#### Run frontend:
```
cd frontend/epi-seek-frontend
npm run dev
```

Visit http://localhost:5173/.
