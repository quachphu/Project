# Nvidia-NIM
# 🚀 NVIDIA RAG Assistant

A sophisticated **Retrieval-Augmented Generation (RAG)** application powered by **NVIDIA AI Endpoints** and **LangChain** for intelligent document question-answering.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-latest-green.svg)
![NVIDIA](https://img.shields.io/badge/NVIDIA-AI%20Endpoints-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### 🤖 **Advanced AI Models**
- Powered by NVIDIA's state-of-the-art language models
- Support for multiple models: Llama 3 70B/8B, Mixtral 8x7B
- Configurable temperature and generation parameters

### 📄 **Multiple Document Sources**
- **PDF Directory**: Process entire directories of PDF files
- **File Upload**: Support for PDF and text file uploads
- **Web Scraping**: Extract content from web URLs
- **Flexible Processing**: Configurable chunk size and overlap

### 🔍 **Intelligent Search**
- Semantic search using FAISS vector database
- NVIDIA embeddings for high-quality document representations
- Context-aware answer generation

### 📊 **Real-time Analytics**
- Track query performance and response times
- Interactive charts and metrics dashboard
- Usage statistics and optimization insights

### 💬 **Interactive Chat Interface**
- Modern, responsive chat UI with animations
- Source document citations
- Chat history management
- Real-time streaming responses

### 🎨 **Beautiful UI/UX**
- Dark mode with gradient backgrounds
- Glassmorphism design elements
- Smooth animations and transitions
- Mobile-responsive layout

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Streamlit |
| **AI Models** | NVIDIA AI Endpoints |
| **Document Processing** | LangChain |
| **Vector Database** | FAISS |
| **Visualizations** | Plotly |
| **PDF Processing** | PyPDF |
| **Web Scraping** | LangChain WebBaseLoader |

## 📋 Prerequisites

- Python 3.8+
- NVIDIA API Key ([Get yours here](https://developer.nvidia.com/))
- pip package manager

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nvidia-rag-assistant.git
cd nvidia-rag-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 4. Run the Application
```bash
streamlit run app2.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Document Upload
1. Navigate to the **"Document Upload"** tab
2. Choose your document source:
   - **PDF Directory**: Enter the path to your PDF folder
   - **Upload Files**: Drag and drop PDF/text files
   - **Web URL**: Enter a webpage URL
3. Click **"Process Documents"** to create embeddings

### Step 2: Ask Questions
1. Go to the **"Chat"** tab
2. Type your question in the input field
3. Click **"Search"** to get AI-powered answers
4. View source documents for context

### Step 3: Monitor Performance
1. Check the **"Analytics"** tab for:
   - Response time trends
   - Query statistics
   - Performance metrics

## ⚙️ Configuration

### Model Selection
Choose from available NVIDIA models:
- `meta/llama3-70b-instruct` (Recommended)
- `meta/llama3-8b-instruct` (Faster)
- `mistralai/mixtral-8x7b-instruct-v0.1`

### Document Processing Parameters
- **Chunk Size**: 100-2000 characters (default: 700)
- **Chunk Overlap**: 0-500 characters (default: 50)
- **Temperature**: 0.0-1.0 (default: 0.7)

## 📁 Project Structure

```
nvidia-rag-assistant/
├── app2.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── us_census/             # Sample PDF directory
├── README.md              # This file
└── docs/                  # Documentation
```

## 🔧 Advanced Features

### Custom Prompting
The application uses optimized prompts for:
- Context-aware responses
- Source attribution
- Concise but thorough answers

### Vector Search Configuration
- **Search Strategy**: Similarity search with k=5
- **Embedding Model**: NVIDIA embeddings
- **Index Type**: FAISS for efficient retrieval

### Performance Optimization
- Caching of embeddings and vector stores
- Async processing for better UX
- Memory-efficient document chunking

## 🎯 Use Cases

- **Research & Analysis**: Query large document collections
- **Customer Support**: AI-powered knowledge base
- **Legal Document Review**: Search through contracts and legal texts
- **Academic Research**: Literature review and citation finding
- **Technical Documentation**: API docs and manual querying

## 🔍 Example Queries

```
"What are the main findings about population growth?"
"Summarize the key statistics from the census data"
"What trends are mentioned in the economic section?"
"Compare the demographic changes between regions"
```

## 🐛 Troubleshooting

### Common Issues

**1. NVIDIA API Key Error**
```
Solution: Ensure your NVIDIA_API_KEY is correctly set in the .env file
```

**2. Memory Issues with Large Documents**
```
Solution: Reduce chunk_size or process documents in smaller batches
```

**3. Slow Response Times**
```
Solution: Try using the llama3-8b-instruct model for faster responses
```

### Performance Tips
- Use smaller chunk sizes for faster processing
- Enable GPU acceleration if available
- Process documents in batches for large collections

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NVIDIA** for providing powerful AI endpoints
- **LangChain** for the excellent RAG framework
- **Streamlit** for the amazing web app framework
- **FAISS** for efficient vector similarity search

## 📞 Support

- 📧 Email: quachphuwork@gmail.com
- 💬 Issues: [GitHub Issues](https://github.com/features/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/nvidia-rag-assistant/wiki)

## 🚀 What's Next?

- [ ] Support for more document formats (DOCX, HTML)
- [ ] Multi-language support
- [ ] Advanced filtering and search options
- [ ] API endpoint for programmatic access
- [ ] Integration with more AI models
- [ ] Collaborative document annotation

---

⭐ **Star this repo if you find it helpful!** ⭐

Made with ❤️ by [Phu Quach](https://github.com/quachphu)
