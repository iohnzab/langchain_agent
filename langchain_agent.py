"""
LangChain AI Agent with Tools and Memory
=========================================
Uses Claude as the LLM with a ReAct-style agent.

Tools included:
  - DuckDuckGo web search
  - Web fetcher (visits and reads a URL directly)
  - Calculator (safe math evaluation)
  - Datetime (current date/time)

Setup:
  pip3 install langchain langchain-anthropic langchain-community ddgs python-dotenv requests beautifulsoup4

Create a .env file in the same folder with:
  ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE

Usage:
  python3 langchain_agent.py
"""

import os
import math
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import requests
from bs4 import BeautifulSoup
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun


# ── 1. LLM ──────────────────────────────────────────────────────────────────

llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
    temperature=0,
    max_tokens=2048,
)


# ── 2. Tools ─────────────────────────────────────────────────────────────────

def fetch_website(url: str) -> str:
    """Visit a URL and return its readable text content."""
    url = url.strip().strip("'\"")

    # Add https:// if missing
    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; LangChainBot/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Trim to avoid token overflow
        lines = [line for line in text.splitlines() if line.strip()]
        content = "\n".join(lines[:150])  # first 150 meaningful lines

        return content if content else "No readable content found on this page."

    except requests.exceptions.SSLError:
        return "SSL error when fetching the website. Try searching for it instead."
    except requests.exceptions.ConnectionError:
        return f"Could not connect to {url}. The site may be down or unreachable."
    except Exception as e:
        return f"Error fetching website: {e}"


def safe_calculator(expression: str) -> str:
    """Evaluate a math expression safely."""
    clean = expression.strip().replace("^", "**")
    safe_namespace = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    safe_namespace["abs"] = abs
    safe_namespace["round"] = round
    try:
        result = eval(clean, {"__builtins__": {}}, safe_namespace)  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


def get_datetime(_: str = "") -> str:
    """Return the current date and time."""
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y. Current time: %H:%M:%S")


search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="fetch_website",
        func=fetch_website,
        description=(
            "Visit and read the actual content of a website or URL. "
            "Use this when the user wants to see what's on a specific website, "
            "portfolio, or any URL like 'example.com', etc. "
            "Input should be the full URL or domain name, e.g. 'https://example.com'."
        ),
    ),
    Tool(
        name="web_search",
        func=search.run,
        description=(
            "Search the web for general information, news, or topics. "
            "Use this for broad searches. For reading a specific website, use fetch_website instead. "
            "Input should be a search query."
        ),
    ),
    Tool(
        name="calculator",
        func=safe_calculator,
        description=(
            "Evaluate mathematical expressions. Input: a math expression like "
            "'(100 + 50) * 0.15' or 'sqrt(144)'."
        ),
    ),
    Tool(
        name="datetime",
        func=get_datetime,
        description=(
            "Get the current date and time. Input can be empty string."
        ),
    ),
]


# ── 3. Prompt ────────────────────────────────────────────────────────────────

REACT_PROMPT = PromptTemplate.from_template(
    """You are a helpful AI assistant named Zab Bot. You are enthusiastic and professional.
When someone says "okay" or "thanks", respond warmly and ask if there's anything else you can help with.

You have access to the following tools:
{tools}

IMPORTANT RULES:
- When the user asks to visit, open, read, or show a website/URL, ALWAYS use fetch_website.
- When the user asks to search for general info or news, use web_search.
- For simple conversational messages (like "okay", "thanks", "hello"), respond directly with Final Answer WITHOUT using any tool.
- Use each tool ONLY ONCE per question. After getting an Observation, go straight to Final Answer.
- You MUST always end with "Final Answer:" — never leave a response without it.

Use this format EXACTLY — do not repeat any step:

Question: the input question you must answer
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: the input
Observation: the result
Thought: I now know the final answer
Final Answer: your answer here

If no tool needed:
Thought: I can answer directly
Final Answer: your answer here

Previous conversation history:
{chat_history}

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
)


# ── 4. Memory ────────────────────────────────────────────────────────────────

memory = ConversationBufferMemory(
    memory_key="chat_history",
    human_prefix="User",
    ai_prefix="Assistant",
    return_messages=False,
)


# ── 5. Agent ──────────────────────────────────────────────────────────────────

agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors="Please output a valid Final Answer immediately.",
    return_intermediate_steps=False,
)


# ── 6. Chat loop ──────────────────────────────────────────────────────────────

def chat(query: str) -> str:
    """Send a query to the agent and return its response."""
    result = agent_executor.invoke({"input": query})
    return result["output"]


def main():
    print("=" * 60)
    print("  LangChain Agent  (type 'quit' or 'exit' to stop)")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Goodbye!")
            break

        try:
            response = chat(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\n[Error] {e}")


if __name__ == "__main__":
    main()