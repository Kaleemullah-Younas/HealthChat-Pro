from flask import Flask, render_template, jsonify, request, session
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from src.prompt import *
import os
import json
import time
import uuid


app = Flask(__name__)
app.secret_key = 'healthchat-pro-secret-key-2024'

# Store chat memories for each session
chat_memories = {}


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


embeddings = download_hugging_face_embeddings()

index_name = "healthchat" 
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)




retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

ChatModel = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    openai_api_key="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",
    openai_api_base="https://openrouter.ai/api/v1",
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(ChatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)



@app.route("/")
def index():
    # Initialize session if needed
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('chat.html')

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    if 'session_id' in session:
        session_id = session['session_id']
        if session_id in chat_memories:
            chat_memories[session_id].clear()
    return jsonify({"status": "success"})

@app.route("/get_history", methods=["GET"])
def get_history():
    if 'session_id' not in session:
        return jsonify({"messages": []})
    
    session_id = session['session_id']
    if session_id not in chat_memories:
        return jsonify({"messages": []})
    
    chat_memory = chat_memories[session_id]
    messages = []
    
    for message in chat_memory.messages:
        if isinstance(message, HumanMessage):
            messages.append({"type": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            messages.append({"type": "bot", "content": message.content})
    
    return jsonify({"messages": messages})



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    
    # Get or create chat memory for this session
    if session_id not in chat_memories:
        chat_memories[session_id] = InMemoryChatMessageHistory()
    
    chat_memory = chat_memories[session_id]
    
    # Get chat history for context
    chat_history = chat_memory.messages
    
    # Create context-aware prompt with chat history
    context_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt + "\n\nPrevious conversation context: {chat_history}"),
        ("human", "{input}")
    ])
    
    # Format chat history for context
    history_text = ""
    for message in chat_history[-6:]:  # Last 6 messages for context
        if isinstance(message, HumanMessage):
            history_text += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            history_text += f"Assistant: {message.content}\n"
    
    # Create chain with context
    context_chain = create_stuff_documents_chain(ChatModel, context_prompt)
    context_rag_chain = create_retrieval_chain(retriever, context_chain)
    
    # Get response
    response = context_rag_chain.invoke({
        "input": msg,
        "chat_history": history_text
    })
    
    # Save to memory
    chat_memory.add_messages([
        HumanMessage(content=msg),
        AIMessage(content=response["answer"])
    ])
    
    # Prepare response with sources
    sources = []
    if "context" in response:
        for doc in response["context"]:
            if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                sources.append({
                    "source": doc.metadata.get('source', 'Unknown'),
                    "page": doc.metadata.get('page', 'N/A'),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
    
    return jsonify({
        "answer": response["answer"],
        "sources": sources,
        "session_id": session_id
    })



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)