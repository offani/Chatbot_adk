"""
Multi-Agent Intelligent Assistant - Root Agent Configuration

This file exposes the root_agent for the Google ADK CLI tools (adk web, adk run).
The root_agent is a SupervisorAgent that coordinates between specialized sub-agents.
"""

import os
from dotenv import load_dotenv

from .agents.web_search_agent import create_web_search_agent
from .agents.multimodal_agent import create_multimodal_agent
from .agents.supervisor_agent import create_supervisor_agent

# Load environment variables
load_dotenv()

# Initialize specialist agents
web_search_agent = create_web_search_agent()
multimodal_agent = create_multimodal_agent()

# Create the root agent (Supervisor/Coordinator)
# This is what ADK CLI tools will use
root_agent = create_supervisor_agent(web_search_agent, multimodal_agent)

# Agent metadata for ADK
__all__ = ['root_agent']
