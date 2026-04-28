import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import os
from dotenv import load_dotenv

# Adding override=True forces Python to read the fresh .env file 
# instead of any cached keys stuck in your terminal's memory.
load_dotenv(override=True)

# 1. Isolate the Unstructured Text Data
df = pd.read_csv('lumentum_synthetic_hr.csv')
# We only want to vectorize actual exit interviews, ignoring active employees
exit_interviews = df[df['Voluntary_Turnover'] == 'Yes']['Exit_Interview'].tolist()

# 2. Text Chunking
# Splitting long text into smaller pieces so the AI can digest it
text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
documents = text_splitter.create_documents(exit_interviews)

# 3. Vectorization & Database Creation
print("Vectorizing exit interviews into FAISS database...")
embeddings = OpenAIEmbeddings()
# FAISS stores the text as mathematical coordinates
vector_store = FAISS.from_documents(documents, embeddings)

# Save the vector database locally so the dashboard can load it
vector_store.save_local("faiss_hr_index")
print("File 3 Complete: RAG Vector Database built and saved.")