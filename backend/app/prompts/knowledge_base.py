from typing import Dict, Any
from app.models.project import Project
from app.models.documentation_item import DocumentationItem


def get_system_prompt() -> str:
    """Get the system prompt for knowledge base updates."""
    return """You are a knowledge management assistant for a Business Analyst documentation system.
Your role is to maintain a concise, cumulative project knowledge base.

The knowledge base should capture key information useful for generating future documentation:
- Stakeholders and their roles
- Business rules and constraints
- Technical decisions and rationale
- Domain terminology and definitions
- Dependencies and integrations
- Common patterns or requirements

Be concise but comprehensive. Avoid duplication. Integrate new information with existing context."""


def get_user_prompt(
    project: Project,
    item: DocumentationItem,
    generated_content: Dict[str, Any],
    questions_and_answers: list
) -> str:
    """
    Build the prompt for updating knowledge base.

    Args:
        project: The project
        item: The documentation item just completed
        generated_content: The generated documentation
        questions_and_answers: List of Q&A tuples

    Returns:
        Formatted prompt
    """
    # Format Q&A
    qa_text = "\n".join([
        f"Q: {qa['question']}\nA: {qa['answer']}"
        for qa in questions_and_answers
    ])

    # Format generated content summary
    content_type = item.type.value
    content_summary = f"Type: {content_type}\nTitle: {item.title}"

    prompt = f"""Update the project knowledge base with insights from newly created documentation.

**Current Knowledge Base:**
{project.knowledge_base if project.knowledge_base else "Empty - this is the first documentation item."}

**New Documentation Created:**
- Type: {item.type.value}
- Title: {item.title}
- Description: {item.description}

**Key Questions and Answers:**
{qa_text}

**Generated Content Summary:**
{str(generated_content)[:500]}...

Integrate the new information into the existing knowledge base.
Focus on facts that will help generate future documentation:
- New stakeholders mentioned
- Business rules or constraints identified
- Technical decisions or requirements
- Domain-specific terminology
- Dependencies or integrations
- Patterns that might apply to other features

Keep the knowledge base concise (max 1000 words). Remove outdated information if needed.
Return ONLY the updated knowledge base text (no meta-commentary)."""

    return prompt


def get_response_schema() -> Dict[str, Any]:
    """
    Get the JSON schema for knowledge base update response.

    Returns:
        JSON schema dictionary
    """
    return {
        "type": "object",
        "properties": {
            "knowledge_base": {
                "type": "string",
                "description": "Updated cumulative knowledge base for the project"
            }
        },
        "required": ["knowledge_base"],
        "additionalProperties": False
    }
