# 🤖 LangChain AI Agent

A conversational AI agent built with LangChain and Claude (Anthropic), capable of browsing websites, searching the web, doing math, and remembering your conversation.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 🌐 **fetch_website** | Visits and reads the actual content of any URL |
| 🔍 **web_search** | Searches the web via DuckDuckGo for news and general info |
| 🧮 **calculator** | Evaluates math expressions (`sqrt`, `%`, `**`, etc.) |
| 📅 **datetime** | Returns the current date and time |
| 🧠 **memory** | Remembers the conversation within a session |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/iohnzab/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip3 install langchain langchain-anthropic langchain-community ddgs python-dotenv requests beautifulsoup4
```

### 3. Set up your API key

Create a `.env` file in the project folder:

```
ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE
```

> Get your API key at [console.anthropic.com](https://console.anthropic.com)

### 4. Run the agent

```bash
python3 langchain_agent.py
```

---

## 💬 Example Usage

```
You: read iohnzab.info
Agent: The website contains information about John Anthony Zabala Jr.,
       an AI Automation Software Engineer...

You: what is 15% of 3500?
Agent: 15% of 3500 is 525.

You: what is today's date?
Agent: Today is Friday, April 10, 2026.

You: search latest AI news
Agent: Here are the latest developments in AI...
```

---

## 🗂 Project Structure

```
LangChain/
├── langchain_agent.py   # Main agent script
├── .env                 # Your API key (never commit this!)
├── .gitignore           # Excludes .env from git
└── README.md            # This file
```

---

## ⚠️ Important

Never commit your `.env` file to GitHub. Make sure your `.gitignore` includes:

```
.env
__pycache__/
*.pyc
```

---

## 🛠 Built With

- [LangChain](https://www.langchain.com/) — Agent framework
- [Anthropic Claude](https://www.anthropic.com/) — LLM (claude-3-haiku)
- [DuckDuckGo Search](https://pypi.org/project/ddgs/) — Web search
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) — Web scraping
- [Python Dotenv](https://pypi.org/project/python-dotenv/) — Environment variables

---

## 👤 Author

**John Anthony Zabala Jr.**
- Website: [iohnzab.info](https://iohnzab.info)
- GitHub: [@iohnzab](https://github.com/iohnzab)
