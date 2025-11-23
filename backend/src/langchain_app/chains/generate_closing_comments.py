from src.langchain_app.config.model_config import get_llm
from langchain_core.output_parsers import JsonOutputParser
from src.schemas.closing_comments import ClosingComments

import json

parser = JsonOutputParser(pydantic_object=ClosingComments)

async def generate_closing_comments(ticket_data: dict) -> str:
    """
    Generate closing comments for a ticket using AI.
    
    Raises:
        ValueError: If GOOGLE_API_KEY is not configured.
    """
    # Get LLM instance (will raise ValueError if API key not configured)
    llm = get_llm()
    
    content = (
        f"Ticket Title: {ticket_data['title']}\n"
        f"Description: {ticket_data['description']}\n"
        f"Category: {ticket_data['category']}\n"
        f"Subcategory: {ticket_data['subcategory']}\n"
        f"Tags: {', '.join(ticket_data['tags'])}\n"
        f"Comments:\n" + "\n".join(ticket_data["comments"])
    )

    messages = [
        {"role": "system", "content": """You are a helpful assistant that generates closing comments for the agent based on the ticket information. 
         output in json:
         {"reason": "", "comment": ""}

         """},
        {"role": "user", "content": f"Please summarize the following ticket:\n{content}"}
    ]

    chain = llm | parser

    response = await chain.ainvoke(messages)

    return response