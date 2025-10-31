import os
import time
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --------------------------------------------------------------------
# ✅ CONFIGURATION
# --------------------------------------------------------------------
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Set this in your Space secrets
REVIEWS_CSV_PATH = "reviews.csv"
REVIEWS_CHROMA_PATH = "chroma_data_gg"

# --------------------------------------------------------------------
# ✅ PROMPT SETUP
# --------------------------------------------------------------------
review_template_str = """
You are a professional hospital data analyst.
You must answer user questions **only** using the context below, which comes from real patient reviews.
If the answer is not clearly supported by this data, reply:
"I don’t have enough information in the hospital reviews to answer that."

Guidelines:
- Stay factual, concise, and neutral.
- Do NOT invent or assume information beyond the reviews.
- Keep your answer under 500 characters.
{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=review_template_str,
    )
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)

review_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=[review_system_prompt, review_human_prompt],
)

# --------------------------------------------------------------------
# ✅ EMBEDDINGS + DATABASE SETUP
# --------------------------------------------------------------------
embedding_function = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Check if Chroma DB already exists; if not, create from CSV
if not os.path.exists(os.path.join(REVIEWS_CHROMA_PATH, "chroma.sqlite3")):
    print("No existing Chroma DB found — creating new one from CSV...")
    loader = CSVLoader(file_path=REVIEWS_CSV_PATH, source_column="review")
    reviews = loader.load()

    reviews_vector_db = Chroma.from_documents(
        documents=reviews,
        embedding=embedding_function,
        persist_directory=REVIEWS_CHROMA_PATH
    )
    reviews_vector_db.persist()
else:
    print("Loading existing Chroma DB...")
    reviews_vector_db = Chroma(
        persist_directory=REVIEWS_CHROMA_PATH,
        embedding_function=embedding_function
    )

# --------------------------------------------------------------------
# ✅ MODEL + RETRIEVAL CHAIN
# --------------------------------------------------------------------
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

reviews_retriever = reviews_vector_db.as_retriever(k=10)

review_chain = (
    {"context": reviews_retriever, "question": RunnablePassthrough()}
    | review_prompt_template
    | chat_model
    | StrOutputParser()
)

# --------------------------------------------------------------------
# ✅ GRADIO CHAT INTERFACE
# --------------------------------------------------------------------
def respond_to_user_question(message, history):
    try:
        response = review_chain.invoke(message)
        return response
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

interface = gr.ChatInterface(
    fn=respond_to_user_question,
    title="🏥 Patient Review Helper Bot",
    description="Ask me anything about patient experiences and hospital feedback — powered by Gemini 2.5 Flash and ChromaDB.",
)

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860)

