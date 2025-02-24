import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain

def initialize_chatbot():
    load_dotenv()
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    embedding_model = "sentence-transformers/all-MiniLM-l6-v2"
    embeddings_folder = "./content/"
    faiss_index_path = "./content/faiss_index"
    hf_model = "mistralai/Mistral-7B-Instruct-v0.3"

    # Load FAISS index
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model,
        cache_folder=embeddings_folder
    )
    vector_db = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})

    # Initialize LLM
    llm = HuggingFaceEndpoint(
        repo_id=hf_model,
        task='text-generation',
        temperature=0.01,
        top_p=0.95,
        repetition_penalty=1.03,
        huggingfacehub_api_token=hf_token
    )

    # Define prompt template
    input_template = """Answer the question based only on the following context. Keep your answers short and succinct.
    
    Context to answer question:
    {context}

    Question to be answered: {input}
    Response:"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", input_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    # Create chains
    doc_retriever = create_history_aware_retriever(llm, retriever, prompt)
    doc_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(doc_retriever, doc_chain)

    return chain

def chat_with_bot(user_input, history, chain, retriever):
    try:
        response = chain.invoke({"input": user_input, "chat_history": history, "context": retriever})
        history.append({"role": "human", "content": user_input})
        history.append({"role": "assistant", "content": response["answer"]})
        return response["answer"], history
    except Exception as e:
        return f"An error occurred: {e}", history
