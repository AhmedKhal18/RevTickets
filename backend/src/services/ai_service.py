from src.langchain_app.chains.summarize_ticket_data import summarize_ticket_data
from src.langchain_app.chains.generate_closing_comments import generate_closing_comments
from .ticket_service import TicketService
from .comment_service import CommentService
from src.schemas.summary import TicketSummaryResponse
from src.schemas.closing_comments import ClosingComments
from fastapi import HTTPException

class AIService:
    @staticmethod
    async def get_ticket_summary(ticket_id: str) -> str:
        ticket = await TicketService.get_ticket(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Fetch comments separately if not linked
        comments = await CommentService.get_comments_by_ticket(ticket_id)

        # Build data for summary
        summary_data = {
            "title": ticket.title,
            "description": ticket.description,
            "category": ticket.category.name if ticket.category else "Uncategorized",
            "subcategory": ticket.subCategory.name if ticket.subCategory else "None",
            "tags": [{"key": tag.key, "value": tag.value } for tag in ticket.tagData] if ticket.tagData else [],
            "comments": [c.content for c in comments],
        }

        # Send to LangChain summary function
        try:
            summary = await summarize_ticket_data(summary_data)
            return TicketSummaryResponse(summary=summary)
        except ValueError as e:
            raise HTTPException(
                status_code=503, 
                detail="AI service is not configured. GOOGLE_API_KEY is required for this feature."
            )
    @staticmethod
    async def get_closing_comments(ticket_id: str) -> str:
        ticket = await TicketService.get_ticket(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Fetch comments separately if not linked
        comments = await CommentService.get_comments_by_ticket(ticket_id)

        data = {
            "title": ticket.title,
            "description": ticket.description,
            "category": ticket.category.name if ticket.category else "Uncategorized",
            "subcategory": ticket.subCategory.name if ticket.subCategory else "None",
            "tags": [{"key": tag.key, "value": tag.value } for tag in ticket.tagData] if ticket.tagData else [],
            "comments": [c.content for c in comments],
        }

        try:
            comment = await generate_closing_comments(data)
            return comment
        except ValueError as e:
            raise HTTPException(
                status_code=503, 
                detail="AI service is not configured. GOOGLE_API_KEY is required for this feature."
            )
