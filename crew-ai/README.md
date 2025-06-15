# YouTube Video To Blog Page Creating Multi-Agent With CrewAI 🎥📝
An intelligent multi-agent system that automatically transforms YouTube videos into engaging blog posts using CrewAI framework. This project leverages the power of AI agents to research video content and create well-structured blog articles.

## 🌟 Features

- **Multi-Agent Architecture**: Utilizes two specialized AI agents working collaboratively
- **YouTube Integration**: Automatically fetches and analyzes video transcriptions from YouTube channels
- **Intelligent Content Generation**: Creates comprehensive blog posts from video content
- **Memory & Caching**: Agents retain information across interactions for better context understanding
- **Sequential Processing**: Ensures proper workflow from research to writing
- **Customizable Output**: Generates markdown files ready for publishing

## 🏗️ Architecture

The system consists of two main agents:

1. **Blog Researcher Agent** 🔍
   - Specializes in extracting relevant video transcriptions
   - Expert in AI, Data Science, Machine Learning, and GenAI topics
   - Provides suggestions and insights from video content

2. **Blog Writer Agent** ✍️
   - Transforms research into compelling narratives
   - Simplifies complex technical topics
   - Creates educational and engaging blog content

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API Key
- Internet connection for YouTube access

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/youtube-to-blog-crewai.git
   cd youtube-to-blog-crewai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🔧 Configuration

### Customizing the YouTube Channel

To target a different YouTube channel, modify the channel handle in `tools.py`:

```python
yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@your_channel_handle')
```

### Adjusting Agent Parameters

You can customize agent behaviors in `agents.py`:
- `verbose`: Set to `True` for detailed execution logs
- `memory`: Enable/disable agent memory
- `allow_delegation`: Control if agents can delegate tasks

### Crew Configuration

Modify crew settings in `crew.py`:
- `max_rpm`: API rate limiting (default: 100 requests/minute)
- `cache`: Enable/disable caching for performance
- `process`: Change from sequential to hierarchical if needed

## 📖 Usage

1. **Basic Usage**
   
   Run the crew with the default topic:
   ```bash
   python crew.py
   ```

2. **Custom Topics**
   
   Modify the topic in `crew.py`:
   ```python
   result = crew.kickoff(inputs={'topic': 'Your Topic Here'})
   ```

3. **Output**
   
   The generated blog post will be saved as `new-blog-post.md` in the project directory.

## 📁 Project Structure

```
youtube-to-blog-crewai/
│
├── agents.py          # Agent definitions and configurations
├── tasks.py           # Task definitions for research and writing
├── tools.py           # YouTube tool initialization
├── crew.py            # Crew orchestration and execution
├── requirements.txt   # Project dependencies
├── .env              # Environment variables (create this file)
├── README.md         # Project documentation
└── new-blog-post.md  # Generated blog output (created after execution)
```

## 🔍 How It Works

1. **Research Phase**: The Blog Researcher agent searches the specified YouTube channel for videos related to the given topic and extracts relevant transcriptions.

2. **Analysis**: The researcher processes the video content, understanding key concepts and important points.

3. **Writing Phase**: The Blog Writer agent takes the research output and crafts a well-structured blog post, making complex topics accessible.

4. **Output Generation**: The final blog post is saved as a markdown file, ready for publishing.

## 📝 Example Output

After running the crew, you'll get a markdown file with:
- Comprehensive summary of the video topic
- Key insights and takeaways
- Well-structured content suitable for blog publishing
- Technical concepts explained in an accessible manner

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is correctly set in the `.env` file
   - Check if the key has sufficient credits

2. **YouTube Access Issues**
   - Verify the YouTube channel handle is correct
   - Check your internet connection

3. **Rate Limiting**
   - Adjust `max_rpm` in `crew.py` if you encounter rate limit errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Future Enhancements

- [ ] Support for multiple YouTube channels
- [ ] Custom blog templates
- [ ] SEO optimization for generated content
- [ ] Integration with blog platforms (WordPress, Medium, etc.)
- [ ] Support for different video platforms
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the amazing multi-agent framework
- [OpenAI](https://openai.com/) for providing the LLM capabilities
- [@krishnaik06](https://www.youtube.com/@krishnaik06) for the default YouTube channel content

## 📧 Contact

For questions or support, please open an issue in the GitHub repository or contact [quachphuwork@example.com].

---

⭐ If you find this project helpful, please give it a star on GitHub!
