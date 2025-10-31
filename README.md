# 🏥 Hospital Review Chatbot — AI-Powered Insights from Patient Feedback  
[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Atharva046/RAG_Chatbot)  

## 📋 Project Overview  
This project is an AI-driven chatbot designed to interpret, analyze and answer user questions based on real patient reviews of hospitals and physicians.  
Leveraging state-of-the-art retrieval-augmented generation (RAG) techniques, it provides accurate, context-aware responses rooted in genuine feedback rather than generic answers.

## 🚀 Features  
- **Context-aware question answering**: Users can ask detailed questions like “What are the most common complaints about hospital X?” or “How do patients rate Dr. Y?” and receive grounded, data-driven responses.  
- **Review summarisation & insights**: The chatbot can summarise themes from large sets of reviews (e.g., positive trends, common issues, patterns in physician feedback).  
- **High-performing LLM integration**: Built on the :contentReference[oaicite:0]{index=0} framework, using :contentReference[oaicite:1]{index=1} for semantic search and :contentReference[oaicite:2]{index=2} for generation — delivering fast, reliable responses.  
- **Structured metadata support**: Each review is augmented with metadata (hospital name, physician name, patient identifier) enabling precise retrieval and analysis.  
- **Professional analytical tone**: Tailored to an enterprise / research audience — responses are concise, evidence-based and avoid hallucination when context is lacking.  
- **Public deploy & demonstration ready**: Live on Hugging Face Spaces (link above) — accessible for stakeholders, recruiters or demo viewers.

## 🛠️ Technical Architecture  
1. **Data ingestion**: Loads a CSV of patient reviews (`reviews.csv`) with columns: `review_id`, `visit_id`, `review`, `physician_name`, `hospital_name`, `patient_name`.  
2. **Pre-processing**: Builds “context” strings combining metadata + review text for each record (e.g. *“Hospital: X | Physician: Y | Review: Z”*).  
3. **Embedding generation**: Uses Google Generative AI embeddings (`models/embedding-001`) to convert text to vectors.  
4. **Vector store**: Persisted via ChromaDB in a folder (e.g., `chroma_data_gg`). Allows fast retrieval of top-k relevant reviews.  
5. **Retrieval & scoring**: Queries the vector store to fetch the most semantically relevant reviews for the user question.  
6. **Prompting & generation**: Uses a custom prompt template designed for a “professional healthcare data analyst” persona. Then passes the retrieved context and question to Gemini 2.5 Flash for answer generation.  
7. **Interface**: A Gradio-based chat interface delivering a smooth conversational experience.  
8. **Hosting**: Deployed on Hugging Face Spaces for easy sharing and live demonstration.
<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/890af1ff-d283-4165-a318-2e98d983783f" />

## 📁 Repository Structure  
├── app.py # Main chatbot application code
├── requirements.txt # Dependencies for installation
├── reviews.csv # Patient review data (with metadata)
├── chroma_data_gg/ # Persisted vector database folder
└── README.md # Project overview & usage

## 🔧 Setup & Usage  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/hospital-review-chatbot.git
   cd hospital-review-chatbot
2. Install requirements:
   pip install -r requirements.txt
3. Set your environment variable:
export GOOGLE_API_KEY=your_google_gemini_api_key
4. Ensure reviews.csv is in the root directory.
5. Run the application:
   python app.py
6. Open the Gradio link printed in console or visit the deployed Space above.

   
---

## 📈 Example Use Cases

💬 *“What do patients think about Dr. Sharma’s communication style?”*  
💬 *“Which hospital received the most positive feedback for cleanliness?”*  
💬 *“Are there recurring complaints about waiting times?”*

---

## 💡 Future Enhancements

- Add **sentiment scoring** and **trend analysis** for reviews.  
- Integrate **multi-hospital comparison** based on patient feedback.  
- Implement **real-time data updates** via APIs.  
- Enhance context filtering for **out-of-scope queries**.

---

## 🔗 Live Demo

👉 Try it here: [**RAG Chatbot on Hugging Face Spaces**](https://huggingface.co/spaces/Atharva046/RAG_Chatbot)

---

## 👤 Author

**Atharva Joshi**  
📧 Email: *atharvajoshi046@gmail.com*  
💼 Project created as part of an advanced GenAI RAG implementation using Gemini models.

---



