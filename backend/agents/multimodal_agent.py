import os
import pandas as pd
from pypdf import PdfReader
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models import Gemini
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

def read_file_content(file_path: str) -> list:
    """
    Reads a file and returns a list of types.Part objects suitable for multimodal processing.
    
    Args:
        file_path: Path to the file to read
    
    Returns:
        List of types.Part objects containing the file content
    """
    if not os.path.exists(file_path):
        return [types.Part(text=f"Error: File not found: {file_path}")]
    
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            mime_type = f"image/{ext[1:]}"
            if ext == '.jpg': 
                mime_type = "image/jpeg"
            return [types.Part.from_bytes(data=image_bytes, mime_type=mime_type)]

        elif ext == '.pdf':
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            return [types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")]

        elif ext in ['.csv', '.xlsx', '.xls']:
            if ext == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            return [types.Part(text=f"File content as table:\n\n{df.to_markdown(index=False)}")]

        elif ext in ['.txt', '.md', '.py', '.json']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [types.Part(text=f"File content:\n\n{content}")]

        else:
            return [types.Part(text=f"Unsupported file extension: {ext}. Supported formats: images (jpg, png, webp), PDF, Excel (csv, xlsx, xls), text (txt, md, py, json)")]
    
    except Exception as e:
        return [types.Part(text=f"Error reading file: {e}")]

def create_multimodal_agent(model_name="gemini-2.5-flash-lite"):
    """
    Factory function to create a MultiModalAgent as a sub-agent.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    model = Gemini(model=model_name, api_key=api_key)
    agent = LlmAgent(
        name="multimodal_agent",
        model=model,
        tools=[read_file_content],
        description="Specialized in analyzing and extracting information from files including images, PDFs, Excel spreadsheets, and text documents. Handles queries that involve uploaded or attached files.",
        instruction="""
        You are a Multi-Modal File Analysis Agent.
        
        Your responsibilities:
        1. Use the 'read_file_content' tool to access and process file content
        2. Analyze images, PDFs, spreadsheets, and text documents
        3. Extract relevant information based on the user's query
        4. Provide clear, accurate analysis of the file content
        
        Supported file formats:
        - Images: JPG, PNG, WebP
        - Documents: PDF
        - Spreadsheets: CSV, Excel (XLSX, XLS)
        - Text: TXT, Markdown, Python, JSON
        
        Always use the tool to read files before analyzing them.
        """
    )
    return agent

if __name__ == "__main__":
    # Test the agent standalone
    try:
        from google.adk.runners import InMemoryRunner
        import uuid
        
        agent = create_multimodal_agent()
        runner = InMemoryRunner(agent=agent, app_name="test")
        session_id = str(uuid.uuid4())
        
        runner.session_service.create_session_sync(app_name="test", user_id="user", session_id=session_id)
        
        # Test with a simple query (would need actual file for full test)
        user_msg = types.Content(
            parts=[types.Part(text="What file formats do you support?")], 
            role="user"
        )
        
        response_text = ""
        for event in runner.run(user_id="user", session_id=session_id, new_message=user_msg):
            if hasattr(event, 'text') and event.text:
                response_text += event.text
            elif hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
        
        print("\n[Test Response]:", response_text)
    except Exception as e:
        print(f"Test failed: {e}")
