import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models import Gemini
from dotenv import load_dotenv

load_dotenv()

def create_supervisor_agent(web_search_agent, multimodal_agent, model_name="gemini-2.5-flash-lite"):
    """
    Factory function to create a SupervisorAgent as a coordinator with sub-agents.
    
    This implements the ADK Coordinator/Dispatcher pattern where the coordinator
    routes requests to specialized agents using LLM-driven delegation.
    
    Args:
        web_search_agent: The WebSearchAgent instance
        multimodal_agent: The MultiModalAgent instance
        model_name: The Gemini model to use
    
    Returns:
        LlmAgent configured as a coordinator
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    model = Gemini(model=model_name, api_key=api_key)
    
    # Create coordinator agent with sub-agents for LLM-driven delegation
    coordinator = LlmAgent(
        name="supervisor_agent",
        model=model,
        description="Coordinator that routes queries to specialized agents.",
        instruction="""
        You are the Supervisor. Route user queries to the right specialist:
        
        - web_search_agent: For internet searches, current events, facts, news, weather
        - multimodal_agent: For analyzing files (images, PDFs, spreadsheets, documents)
        
        ALWAYS delegate to a specialist. Never answer directly.
        """,
        sub_agents=[web_search_agent, multimodal_agent]
    )
    
    return coordinator

# if __name__ == "__main__":
#     # Test the coordinator pattern
#     try:
#         from backend.agents.web_search_agent import create_web_search_agent
#         from backend.agents.multimodal_agent import create_multimodal_agent
#         from google.adk.runners import InMemoryRunner
#         from google.genai import types
#         import uuid
        
#         # Create specialist agents
#         web_agent = create_web_search_agent()
#         multimodal = create_multimodal_agent()
        
#         # Create coordinator
#         supervisor = create_supervisor_agent(web_agent, multimodal)
        
#         # Test with runner
#         runner = InMemoryRunner(agent=supervisor, app_name="test")
#         session_id = str(uuid.uuid4())
        
#         runner.session_service.create_session_sync(app_name="test", user_id="user", session_id=session_id)
        
#         user_msg = types.Content(
#             parts=[types.Part(text="What is the weather in Paris?")], 
#             role="user"
#         )
        
#         print("[Test] Sending query to supervisor...")
#         response_text = ""
#         for event in runner.run(user_id="user", session_id=session_id, new_message=user_msg):
#             if hasattr(event, 'text') and event.text:
#                 response_text += event.text
#             elif hasattr(event, 'content') and hasattr(event.content, 'parts'):
#                 for part in event.content.parts:
#                     if part.text:
#                         response_text += part.text
        
#         print("\n[Test Response]:", response_text)
#     except Exception as e:
#         print(f"Test failed: {e}")
#         import traceback
#         traceback.print_exc()
