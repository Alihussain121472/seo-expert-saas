import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import os

class SEORecommendation(BaseModel):
    title: str = Field(description="The task title")
    description: str = Field(description="Detailed explanation of the problem, why it matters, and the recommended fix")
    priority: str = Field(description="One of: Critical, High, Medium, Low")

class AuditResult(BaseModel):
    technical_score: int = Field(description="Score from 0 to 100 based on technical health")
    on_page_score: int = Field(description="Score from 0 to 100 based on on-page SEO")
    overall_score: int = Field(description="Average of technical and on-page score")
    recommendations: list[SEORecommendation] = Field(description="List of actionable SEO tasks")

def run_seo_audit(crawl_data: dict) -> AuditResult:
    """
    Takes crawl data and uses Gemini to analyze it and generate an SEO audit report and tasks.
    """
    # Requires GOOGLE_API_KEY environment variable to be set
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.2)
    
    parser = JsonOutputParser(pydantic_object=AuditResult)
    
    prompt = PromptTemplate(
        template="""You are an expert AI SEO Consultant.
        Analyze the following crawl data for a webpage and identify all SEO problems and opportunities.
        
        Generate an SEO score (0-100) and actionable tasks.
        For every problem, explain: Problem -> Why it matters -> Recommended fix.
        Prioritize them (Critical, High, Medium, Low).
        
        Crawl Data:
        {crawl_data}
        
        \n{format_instructions}""",
        input_variables=["crawl_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    result = chain.invoke({"crawl_data": json.dumps(crawl_data)})
    return AuditResult(**result)
