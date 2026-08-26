import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel
import os

class ChatRequest(BaseModel):
    message: str
    user_id: str
    preferred_language: str = "English" # English, Urdu, Roman Urdu
    context: dict = {} # E.g., user's websites and tasks

def get_seo_manager_response(request: ChatRequest) -> str:
    """
    Acts as the main SEO Manager Agent coordinating user chats.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
    
    # Format the context from the database
    context_str = json.dumps(request.context, indent=2)
    
    system_prompt = f"""You are an Expert AI SEO Manager.
Your goal is to help the user improve their website's organic traffic, explain SEO concepts clearly, and recommend prioritized actions.

USER CONTEXT (from database):
{context_str}

CRITICAL RULES:
1. Always prioritize answering based on the USER CONTEXT provided above (their actual websites, tasks, and SEO audits).
2. If the user asks about their website, check the context. If they have no websites connected, tell them to add one first.
3. Behave like a professional SEO manager + content strategist + technical assistant.
4. You MUST communicate with the user in their preferred language: {request.preferred_language}. 
   - If they ask in Roman Urdu (e.g., "meri website pe traffic kyun nahi aa raha"), you MUST reply in natural Roman Urdu.
5. Do not hallucinate fake analytics. If data is missing in the context, clearly state that you need more data integrations.

Respond to the user's latest message below:
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=request.message)
    ]
    
    response = llm.invoke(messages)
    return response.content
