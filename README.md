# Multi-Agent Intelligent Assistant

A production-ready multi-agent system built with **Google Agent Development Kit (ADK)** that intelligently routes queries to specialized agents for web search and file analysis.

## 🎯 Features

- **🌐 Web Search**: Real-time information retrieval from the internet
- **📄 File Analysis**: Multimodal processing of images, PDFs, spreadsheets, and text
- **🤖 Intelligent Routing**: Automatic query routing using LLM-driven delegation
- **💬 Interactive CLI**: User-friendly command-line interface
- **🔄 Session Management**: Conversation history and context preservation

## 🏗️ Architecture

The system implements the **Coordinator/Dispatcher pattern** with three agents:

- **SupervisorAgent** - Routes queries to appropriate specialists
- **WebSearchAgent** - Searches the web using DuckDuckGo
- **MultiModalAgent** - Analyzes files (images, PDFs, Excel, text)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design and data flows.

## 📋 Requirements

- Python 3.13+
- Google API Key (for Gemini)
- `uv` package manager (recommended) or `pip`

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd acttry

# Install dependencies with uv
uv sync

# Or with pip
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> **Get your API key**: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run the Application

```bash
# With uv
uv run python backend/main.py

# Or with python directly
python backend/main.py
```

## 💡 Usage Examples

### Web Search Queries

```
💬 Your query: What is the capital of France?
📎 File path: [Press Enter]

🤖 Processing...
----------------------------------------------------------
📋 Response: The capital of France is Paris.
```

```
💬 Your query: What's the weather in Tokyo today?
📎 File path: [Press Enter]

🤖 Processing...
----------------------------------------------------------
📋 Response: [Current weather information from web search]
```

### File Analysis

```
💬 Your query: Describe what you see in this image
📎 File path: /path/to/image.jpg

📂 Processing file: /path/to/image.jpg
🤖 Processing...
----------------------------------------------------------
📋 Response: This image shows [detailed description]...
```

```
💬 Your query: Summarize this document
📎 File path: /path/to/document.pdf

📂 Processing file: /path/to/document.pdf
🤖 Processing...
----------------------------------------------------------
📋 Response: [Summary of PDF content]...
```

## 📁 Supported File Formats

| Type | Formats | Description |
|------|---------|-------------|
| **Images** | JPG, JPEG, PNG, WebP | Visual content analysis |
| **Documents** | PDF | Text extraction and summarization |
| **Spreadsheets** | CSV, XLSX, XLS | Data analysis and insights |
| **Text** | TXT, MD, PY, JSON | Code and text analysis |

## 🗂️ Project Structure

```
acttry/
├── backend/
│   ├── agents/
│   │   ├── supervisor_agent.py    # Coordinator agent
│   │   ├── web_search_agent.py    # Web search specialist
│   │   └── multimodal_agent.py    # File analysis specialist
│   └── main.py                     # Application entry point
├── ARCHITECTURE.md                 # System architecture docs
├── README.md                       # This file
├── .env                           # Environment variables
└── pyproject.toml                 # Project dependencies
```

## 🔧 Configuration

### Model Selection

Default model: `gemini-2.5-flash-lite`

To use a different model, modify the agent factory functions:

```python
# In backend/agents/supervisor_agent.py
supervisor = create_supervisor_agent(
    web_search_agent, 
    multimodal_agent,
    model_name="gemini-2.0-flash"  # Change here
)
```

### Supported Models
- `gemini-2.5-flash-lite` (default, fastest)
- `gemini-2.0-flash` (balanced)
- `gemini-2.0-flash-exp` (experimental features)
- `gemini-2.0-pro` (most capable)

## 🧪 Testing

### Test Individual Agents

```bash
# Test WebSearchAgent
uv run python backend/agents/web_search_agent.py

# Test MultiModalAgent
uv run python backend/agents/multimodal_agent.py

# Test SupervisorAgent
uv run python backend/agents/supervisor_agent.py
```

### Example Test Queries

**Web Search**:
- "What is the capital of" France?"
- "Current weather in London"
- "Latest news about AI"

**File Analysis**:
- Provide an image + "Describe this image"
- Provide a PDF + "Summarize this document"
- Provide Excel file + "Analyze this data"

## 🛠️ Troubleshooting

### Common Issues

**Error: GOOGLE_API_KEY not found**
```
Solution: Create a .env file with your Google API key
```

**ModuleNotFoundError**
```bash
Solution: Install dependencies
uv sync
# or
pip install -r requirements.txt
```

**File not found error**
```
Solution: Ensure the file path is absolute and file exists
Example: /Users/username/Documents/file.pdf (not ~/Documents/file.pdf)
```

**No search results**
```
Solution: Check internet connection. DuckDuckGo may be temporarily unavailable.
```

## 🔐 Security & Privacy

- **API Keys**: Stored in `.env` file (never commit to version control)
- **Web Search**: Uses DuckDuckGo (privacy-focused, no tracking)
- **File Processing**: All file processing happens locally
- **Data**: No data is stored or transmitted except to Google's Gemini API

## 📚 Dependencies

Core dependencies:
- `google-genai>=1.52.0` - Google ADK and Gemini integration
- `duckduckgo-search>=8.1.1` - Web search capabilities
- `python-dotenv>=1.2.1` - Environment variable management
- `pandas>=2.3.3` - Data processing
- `pypdf>=6.4.0` - PDF reading
- `pillow>=12.0.0` - Image processing
- `openpyxl>=3.1.5` - Excel file support

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more specialist agents (e.g., code analysis, database queries)
- Implement caching for search results
- Add streaming responses
- Create web UI
- Add unit tests

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- Built with [Google Agent Development Kit (ADK)](https://ai.google.dev/adk)
- Powered by [Gemini LLM](https://ai.google.dev/gemini-api)
- Web search via [DuckDuckGo](https://duckduckgo.com)

## 📞 Support

For issues and questions:
1. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system details
2. Review the troubleshooting section above
3. Open an issue on GitHub

---

**Version**: 1.0  
**Last Updated**: 2025-11-23
