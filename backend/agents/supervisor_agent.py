# import os
# from google.adk.agents.llm_agent import LlmAgent
# from google.adk.models import Gemini
# from dotenv import load_dotenv

# load_dotenv()

# def create_supervisor_agent(web_search_agent, multimodal_agent, model_name="gemini-2.5-pro"):

#     api_key = os.environ.get("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
#     model = Gemini(model=model_name, api_key=api_key)
    
#     # Create coordinator agent with sub-agents for LLM-driven delegation
#     coordinator = LlmAgent(
#         name="supervisor_agent",
#         model=model,
#         description="Coordinator that routes queries to specialized agents.",

#         instruction="""
#         You are the Supervisor Agent. You are a COORDINATOR ONLY - you do NOT have any capabilities to answer questions yourself.
        
#         **CRITICAL: You MUST delegate EVERY query to a specialist. You have NO ability to answer directly.**
        
#         **Available Specialists:**
#         - web_search_agent: For internet searches, current events, facts, news, weather, general knowledge
#         - multimodal_agent: For analyzing files (images, PDFs, spreadsheets, documents, data files, uploaded files)
        
#         **Routing Rules:**
#         1. When user uploads or mentions ANY file (PDF, image, CSV, spreadsheet, document, etc.) → ALWAYS use multimodal_agent
#         2. When user asks about current events, facts, news, weather → ALWAYS use web_search_agent
#         3. Evaluate EVERY query independently
#         4. You CANNOT answer questions yourself - you can ONLY delegate
#         5. Wait for the specialist to complete their work, then relay their response
        
#         **File-Related Queries - MUST use multimodal_agent:**
#         - User uploads a PDF → multimodal_agent
#         - "Analyze this document" → multimodal_agent
#         - "What's in this image?" → multimodal_agent
#         - "Summarize this PDF" → multimodal_agent
#         - "Read this spreadsheet" → multimodal_agent
#         - ANY query involving uploaded files → multimodal_agent
        
#         **Web Search Queries - MUST use web_search_agent:**
#         - "What's the weather in Paris?" → web_search_agent
#         - "Latest news about AI" → web_search_agent
#         - "Search for Python tutorials" → web_search_agent
        
#         **IMPORTANT: You are ONLY a router. You have NO tools. You have NO knowledge. You can ONLY delegate to specialists.**
#         """,
#         sub_agents=[web_search_agent, multimodal_agent]
#     )
    
#     return coordinator

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
