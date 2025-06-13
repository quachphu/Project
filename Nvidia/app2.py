import streamlit as st
import os
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import WebBaseLoader, PyPDFDirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
os.environ['NVIDIA_API_KEY'] = os.getenv("NVIDIA_API_KEY")

# Page configuration
st.set_page_config(
    page_title="NVIDIA RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        color: #ffffff;
    }
    
    /* Title styling */
    .title-container {
        background: linear-gradient(90deg, #00ff88 0%, #00a8ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 2rem;
        padding: 1rem;
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 255, 136, 0.2);
        border-color: rgba(0, 255, 136, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #00ff88 0%, #00a8ff 100%);
        color: #000000;
        font-weight: 600;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 30px rgba(0, 255, 136, 0.5);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #ffffff;
        border-radius: 10px;
        padding: 0.8rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
    }
    
    /* Success/Info messages */
    .success-msg {
        background: linear-gradient(90deg, rgba(0, 255, 136, 0.2), rgba(0, 168, 255, 0.2));
        border-left: 4px solid #00ff88;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(0, 168, 255, 0.2), rgba(0, 255, 136, 0.2));
        border-left: 4px solid #00a8ff;
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00ff88;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ff88 0%, #00a8ff 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectors" not in st.session_state:
    st.session_state.vectors = None
if "processing_time" not in st.session_state:
    st.session_state.processing_time = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None
if "document_count" not in st.session_state:
    st.session_state.document_count = 0

# Helper functions
def initialize_embeddings():
    """Initialize NVIDIA embeddings"""
    if st.session_state.embeddings is None:
        st.session_state.embeddings = NVIDIAEmbeddings()
    return st.session_state.embeddings

def load_documents(source_type, source_path=None, uploaded_files=None):
    """Load documents from various sources"""
    docs = []
    
    if source_type == "PDF Directory":
        loader = PyPDFDirectoryLoader(source_path)
        docs = loader.load()
    elif source_type == "Uploaded PDFs" and uploaded_files:
        for file in uploaded_files:
            with open(f"temp_{file.name}", "wb") as f:
                f.write(file.getbuffer())
            loader = PyPDFLoader(f"temp_{file.name}")
            docs.extend(loader.load())
            os.remove(f"temp_{file.name}")
    elif source_type == "Web URL" and source_path:
        loader = WebBaseLoader(source_path)
        docs = loader.load()
    elif source_type == "Text File" and uploaded_files:
        for file in uploaded_files:
            content = str(file.read(), "utf-8")
            with open(f"temp_{file.name}", "w") as f:
                f.write(content)
            loader = TextLoader(f"temp_{file.name}")
            docs.extend(loader.load())
            os.remove(f"temp_{file.name}")
    
    return docs

def create_vector_store(docs, embeddings):
    """Create FAISS vector store from documents"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    splits = text_splitter.split_documents(docs)
    vector_store = FAISS.from_documents(splits, embeddings)
    
    return vector_store, len(splits)

# Main UI
st.markdown('<h1 class="title-container">🚀 NVIDIA RAG Assistant</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select Model",
        ["meta/llama3-70b-instruct", "meta/llama3-8b-instruct", "mistralai/mixtral-8x7b-instruct-v0.1"],
        help="Choose the NVIDIA model for generation"
    )
    
    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    
    # Chunk configuration
    st.markdown("### 📄 Document Processing")
    chunk_size = st.number_input("Chunk Size", 100, 2000, 700, 100)
    chunk_overlap = st.number_input("Chunk Overlap", 0, 500, 50, 10)
    
    # Statistics
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Queries", st.session_state.query_count)
    with col2:
        st.metric("Documents", st.session_state.document_count)
    
    if st.session_state.processing_time:
        avg_time = sum(st.session_state.processing_time) / len(st.session_state.processing_time)
        st.metric("Avg Response Time", f"{avg_time:.2f}s")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📤 Document Upload", "📈 Analytics", "ℹ️ About"])

with tab1:
    # Chat Interface
    st.markdown("### 🤖 Ask me anything about your documents!")
    
    # Chat history display
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 **You:** {message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai-message">🤖 **Assistant:** {message["content"]}</div>', 
                       unsafe_allow_html=True)
    
    # Query input
    query = st.text_input("Enter your question:", key="query_input", 
                         placeholder="What would you like to know about your documents?")
    
    col1, col2, col3 = st.columns([5,5,0.1])
    with col1:
        if st.button("🔍 Search", use_container_width=True):
            if query and st.session_state.vectors:
                with st.spinner("🔮 Thinking..."):
                    # Initialize LLM
                    llm = ChatNVIDIA(model=model_name, temperature=temperature)
                    
                    # Create prompt
                    prompt = ChatPromptTemplate.from_template("""
                    You are a helpful AI assistant. Answer the question based on the provided context.
                    Be concise but thorough. If the answer isn't in the context, say so.
                    
                    Context: {context}
                    
                    Question: {input}
                    
                    Answer:
                    """)
                    
                    # Create chains
                    document_chain = create_stuff_documents_chain(llm, prompt)
                    retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 5})
                    retrieval_chain = create_retrieval_chain(retriever, document_chain)
                    
                    # Get response
                    start_time = time.time()
                    response = retrieval_chain.invoke({'input': query})
                    end_time = time.time()
                    
                    # Update statistics
                    response_time = end_time - start_time
                    st.session_state.processing_time.append(response_time)
                    st.session_state.query_count += 1
                    
                    # Add to chat history
                    st.session_state.messages.append({"role": "user", "content": query})
                    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                    
                    # Display response
                    st.markdown(f'<div class="success-msg">✅ Response generated in {response_time:.2f} seconds</div>', 
                               unsafe_allow_html=True)
                    
                    # Show relevant documents
                    with st.expander("📚 Source Documents", expanded=False):
                        for i, doc in enumerate(response["context"]):
                            st.markdown(f"**Document {i+1}:**")
                            st.markdown(f'<div class="metric-card">{doc.page_content}</div>', 
                                       unsafe_allow_html=True)
                    
                    # Rerun to update chat display
                    st.rerun()
            else:
                st.error("⚠️ Please upload documents first!")
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

with tab2:
    # Document Upload Interface
    st.markdown("### 📁 Document Management")
    
    source_type = st.selectbox(
        "Select Document Source",
        ["PDF Directory", "Uploaded PDFs", "Web URL", "Text File"]
    )
    
    uploaded_files = None
    source_path = None
    
    if source_type == "PDF Directory":
        source_path = st.text_input("Enter directory path:", value="./us_census")
    elif source_type in ["Uploaded PDFs", "Text File"]:
        file_type = "pdf" if source_type == "Uploaded PDFs" else "txt"
        uploaded_files = st.file_uploader(
            f"Upload {file_type.upper()} files",
            type=[file_type],
            accept_multiple_files=True
        )
    elif source_type == "Web URL":
        source_path = st.text_input("Enter URL:", placeholder="https://example.com")
    
    if st.button("🚀 Process Documents", use_container_width=True):
        if (source_path or uploaded_files):
            with st.spinner("📥 Loading documents..."):
                embeddings = initialize_embeddings()
                
                # Progress tracking
                progress = st.progress(0)
                status = st.empty()
                
                # Load documents
                status.text("Loading documents...")
                progress.progress(25)
                docs = load_documents(source_type, source_path, uploaded_files)
                
                if docs:
                    # Create vector store
                    status.text("Creating embeddings...")
                    progress.progress(50)
                    
                    st.session_state.vectors, chunk_count = create_vector_store(docs, embeddings)
                    st.session_state.document_count = len(docs)
                    
                    progress.progress(100)
                    status.text("✅ Processing complete!")
                    
                    # Display success metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Documents Processed", len(docs))
                    with col2:
                        st.metric("Text Chunks Created", chunk_count)
                    with col3:
                        st.metric("Vector Store", "Ready ✅")
                    
                    st.success("🎉 Documents successfully processed and indexed!")
                else:
                    st.error("❌ No documents found. Please check your source.")
        else:
            st.warning("⚠️ Please provide a document source.")

with tab3:
    # Analytics Dashboard
    st.markdown("### 📊 Performance Analytics")
    
    if st.session_state.processing_time:
        # Response time chart
        fig_time = go.Figure()
        fig_time.add_trace(go.Scatter(
            x=list(range(1, len(st.session_state.processing_time) + 1)),
            y=st.session_state.processing_time,
            mode='lines+markers',
            name='Response Time',
            line=dict(color='#00ff88', width=3),
            marker=dict(size=8)
        ))
        fig_time.update_layout(
            title="Query Response Times",
            xaxis_title="Query Number",
            yaxis_title="Response Time (seconds)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_time, use_container_width=True)
        
        # Statistics summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Min Response Time", f"{min(st.session_state.processing_time):.2f}s")
        with col2:
            st.metric("Max Response Time", f"{max(st.session_state.processing_time):.2f}s")
        with col3:
            st.metric("Avg Response Time", f"{sum(st.session_state.processing_time)/len(st.session_state.processing_time):.2f}s")
        with col4:
            st.metric("Total Processing Time", f"{sum(st.session_state.processing_time):.2f}s")
    else:
        st.info("📊 Analytics will appear here after you start querying documents.")

with tab4:
    # About Section
    st.markdown("""
    ### 🌟 About NVIDIA RAG Assistant
    
    <div class="metric-card">
    <h4>🚀 Features</h4>
    
    - **🤖 Advanced AI Models**: Powered by NVIDIA's state-of-the-art language models
    - **📄 Multiple Document Sources**: Support for PDFs, text files, and web pages
    - **🔍 Intelligent Search**: Semantic search using FAISS vector database
    - **📊 Real-time Analytics**: Track performance and usage statistics
    - **💬 Chat Interface**: Interactive conversation with document context
    - **🎨 Modern UI**: Beautiful, responsive design with animations
    
    </div>
    
    <div class="metric-card" style="margin-top: 1rem;">
    <h4>🛠️ Technology Stack</h4>
    
    - **LangChain**: For document processing and chain creation
    - **NVIDIA AI Endpoints**: For embeddings and language generation
    - **FAISS**: For efficient vector similarity search
    - **Streamlit**: For the web interface
    - **Plotly**: For interactive visualizations
    
    </div>
    
    <div class="metric-card" style="margin-top: 1rem;">
    <h4>📝 How to Use</h4>
    
    1. **Upload Documents**: Go to the "Document Upload" tab and select your source
    2. **Process**: Click "Process Documents" to create embeddings
    3. **Ask Questions**: Switch to the "Chat" tab and start asking questions
    4. **View Analytics**: Check the "Analytics" tab for performance metrics
    
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: rgba(255,255,255,0.6);">Built with ❤️ using NVIDIA AI | Powered by LangChain & Streamlit</p>
</div>
""", unsafe_allow_html=True)