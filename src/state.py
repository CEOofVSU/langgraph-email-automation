from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated

# Convert Email from Pydantic BaseModel to TypedDict
class Email(TypedDict):
    id: str  # Unique identifier of the email
    threadId: str  # Thread identifier of the email
    messageId: str  # Message identifier of the email
    references: str  # References of the email
    sender: str  # Email address of the sender
    subject: str  # Subject line of the email
    body: str  # Body content of the email

class GraphState(TypedDict):
    emails: List[Email]
    current_email: Email
    email_category: str
    generated_email: str
    rag_queries: List[str]
    retrieved_documents: str
    writer_messages: Annotated[list, add_messages]
    sendable: bool
    trials: int

# Helper functions to create Email objects (since we can't use Pydantic validation anymore)
def create_email(
    id: str,
    threadId: str,
    messageId: str,
    references: str,
    sender: str,
    subject: str,
    body: str
) -> Email:
    """Helper function to create an Email object with validation"""
    return Email(
        id=id,
        threadId=threadId,
        messageId=messageId,
        references=references,
        sender=sender,
        subject=subject,
        body=body
    )

def validate_email_data(email_data: Dict[str, Any]) -> Email:
    """Helper function to validate and convert dict to Email TypedDict"""
    required_fields = ['id', 'threadId', 'messageId', 'references', 'sender', 'subject', 'body']
    
    for field in required_fields:
        if field not in email_data:
            raise ValueError(f"Missing required field: {field}")
    
    return Email(
        id=str(email_data['id']),
        threadId=str(email_data['threadId']),
        messageId=str(email_data['messageId']),
        references=str(email_data['references']),
        sender=str(email_data['sender']),
        subject=str(email_data['subject']),
        body=str(email_data['body'])
    )
