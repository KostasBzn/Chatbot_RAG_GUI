# Chatbot with RAG (Retrieval-Augmented Generation)

This project implements a chatbot using Retrieval-Augmented Generation (RAG) with Streamlit for the user interface. The chatbot is trained on a PDF document and uses Hugging Face models for embeddings and text generation.

## Features

- **Document Training**: Train the chatbot on a custom PDF file.
- **Chat Interface**: Interact with the chatbot via a Streamlit web app.
- **RAG Architecture**: Combines retrieval-based and generative AI for accurate and context-aware responses.

## Prerequisites

- Python 3.8 or higher
- A Hugging Face API token (sign up at [Hugging Face](https://huggingface.co/))

## How to Run the Chat Bot

1. Clone the repository or download the files.
2. Navigate to the folder containing the chat-bot files.
3. Install the required libraries: `pip install -r requirements.txt`
4. Create a .env file in the root directory and add your Hugging Face API token: `HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here`
5. Run `python train_bot.py` to train the chat bot. This will generate a FAISS index in the ./content/ directory.
6. Run the Chatbot App with `streamlit run app.py`

## Customization

- `Change the PDF File`: Replace ISLP_website.pdf in the ./data/ directory with your desired file. Update the pdf_path variable in train_bot.py if necessary and retrain your chat with new content.
- `Adjust Chunk Size`: Modify the chunk_size and chunk_overlap parameters in train_bot.py to control how the document is split.
- `Update the Model`: Change the hf_model variable in chat_bot.py to use a different Hugging Face model.
