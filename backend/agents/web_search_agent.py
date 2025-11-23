import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import google_search
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

# def web_search_tool(query: str) -> str:
#     """
#     Performs a web search using DuckDuckGo to find information about the query.
#     Args:
#         query: The search query string.
#     Returns:
#         A string containing the search results.
#     """
#     print(f"[Web Search Tool] Searching for: {query}")
#     try:
#         with DDGS() as ddgs:
#             results = list(ddgs.text(query, max_results=5))
#         if not results:
#             return "No search results found."
        
#         # Format results nicely
#         formatted = []
#         for i, result in enumerate(results, 1):
#             formatted.append(f"{i}. {result.get('title', 'No title')}\n   {result.get('body', 'No description')}\n   URL: {result.get('href', '')}")
#         return "\n\n".join(formatted)
#     except Exception as e:
#         return f"Error performing search: {e}"

def create_web_search_agent(model_name="gemini-2.5-flash-lite"):
    """
    Factory function to create a WebSearchAgent as a sub-agent.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    model = Gemini(model=model_name, api_key=api_key)
    agent = LlmAgent(
        name="web_search_agent",
        model=model,
        tools=[google_search],
        description="Specialized in retrieving information from the internet using web search. Handles queries about current events, facts, news, weather, and general knowledge that requires external information.",
        instruction="""
        You are a Web Search Agent specialized in finding information on the internet.
        
        Your responsibilities:
        1. Use the 'web_search_tool' to find relevant and up-to-date information
        2. Synthesize search results into clear, accurate, and concise answers
        3. Cite sources when appropriate
        4. If search results are insufficient, state what you found and what's missing
        
        Always provide well-structured, informative responses based on the search results.
        """
    )
    return agent

