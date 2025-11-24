"""
Quick test script to verify multi-agent delegation works correctly
"""
import sys
sys.path.append('backend')

from agents.supervisor_agent import create_supervisor_agent
from agents.web_search_agent import create_web_search_agent  
from agents.multimodal_agent import create_multimodal_agent
from google.adk.runners import InMemoryRunner
from google.genai import types
import uuid

# Create agents
print("Creating agents...")
web_agent = create_web_search_agent()
multimodal_agent = create_multimodal_agent()
supervisor = create_supervisor_agent(web_agent, multimodal_agent)

print(f"OK: Supervisor has {len(supervisor.sub_agents)} sub-agents")
print(f"OK: Sub-agents: {[agent.name for agent in supervisor.sub_agents]}")

# Create runner
runner = InMemoryRunner(agent=supervisor, app_name="test")
session_id = str(uuid.uuid4())
runner.session_service.create_session_sync(app_name="test", user_id="user", session_id=session_id)

# Test 1: Web Search Query
print("\n" + "="*60)
print("TEST 1: Web Search Query")
print("="*60)
query = "What is quantum computing?"
print(f"Query: {query}")
user_msg = types.Content(parts=[types.Part(text=query)], role="user")

response_text = ""
for event in runner.run(user_id="user", session_id=session_id, new_message=user_msg):
    if hasattr(event, 'text') and event.text:
        response_text += event.text

print(f"\nResponse length: {len(response_text)} chars")
if response_text:
    print("Response preview:")
    print(response_text[:300] + "..." if len(response_text) > 300 else response_text)
    print("\nTEST 1: PASSED")
else:
    print("WARNING: No response received!")

print("\nAll agents loaded successfully!")
