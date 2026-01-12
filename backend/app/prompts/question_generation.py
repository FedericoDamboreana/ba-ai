from typing import Dict, Any
from app.models.project import Project
from app.models.documentation_item import DocumentationItem


def get_system_prompt() -> str:
    """Get the system prompt for question generation."""
    return """You are a senior Business Analyst assistant helping to gather requirements.
Your role is to generate relevant, comprehensive questions that will help create complete and professional documentation.
Maintain a formal, professional tone suitable for German business clients.

Guidelines:
- Generate 8-15 targeted questions that cover all aspects of the requirement
- Avoid false dichotomies in multiple choice questions (always include "Other" mentally or make them text)
- Mark questions as critical only if they're essential for the documentation
- Use conditional questions (trigger_condition) when a question depends on a previous answer
- Questions should be specific and actionable
- Focus on "what" and "why" rather than "how" for high-level docs
- Consider the project context and existing knowledge to avoid redundant questions"""


def get_user_prompt(project: Project, item: DocumentationItem) -> str:
    """
    Build the user prompt with project and item context.

    Args:
        project: The project this item belongs to
        item: The documentation item to generate questions for

    Returns:
        Formatted user prompt string
    """
    doc_type_guidance = {
        "PRD": "Focus on project scope, objectives, stakeholders, constraints, success criteria, and high-level requirements.",
        "Epic": "Focus on business value, user problems being solved, scope boundaries, high-level features, and dependencies.",
        "UserStory": "Focus on the user persona, their goal, the benefit, acceptance criteria scenarios, edge cases, and constraints.",
        "FRS": "Focus on detailed functional requirements, system behavior, inputs/outputs, business rules, validations, and error handling."
    }

    guidance = doc_type_guidance.get(item.type.value, "Focus on comprehensive requirement details.")

    prompt = f"""Generate questions to create a {item.type.value} document.

**Project Context:**
- Project Name: {project.name}
- Client: {project.client or "Not specified"}
- Project Description: {project.description}

**Existing Project Knowledge:**
{project.knowledge_base if project.knowledge_base else "No prior documentation for this project."}

**Documentation Item:**
- Type: {item.type.value}
- Title: {item.title}
- Description: {item.description}

**Guidance for {item.type.value}:**
{guidance}

Generate questions that will help create comprehensive {item.type.value} documentation.
Consider the project context and existing knowledge to avoid asking redundant questions.
Return questions in order of importance."""

    return prompt


def get_response_schema() -> Dict[str, Any]:
    """
    Get the JSON schema for question generation response.

    Returns:
        JSON schema dictionary
    """
    return {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_text": {
                            "type": "string",
                            "description": "The question to ask the user"
                        },
                        "question_type": {
                            "type": "string",
                            "enum": ["Text", "MultipleChoice", "Checkbox"],
                            "description": "Type of question input"
                        },
                        "options": {
                            "anyOf": [
                                {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                {"type": "null"}
                            ],
                            "description": "Options for multiple choice or checkbox questions"
                        },
                        "is_critical": {
                            "type": "boolean",
                            "description": "Whether this question must be answered"
                        },
                        "parent_question_index": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ],
                            "description": "Index of parent question if this is conditional (0-based)"
                        },
                        "required_answer": {
                            "anyOf": [
                                {"type": "string"},
                                {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                {"type": "null"}
                            ],
                            "description": "Required answer(s) from parent to show this question"
                        }
                    },
                    "required": [
                        "question_text",
                        "question_type",
                        "options",
                        "is_critical",
                        "parent_question_index",
                        "required_answer"
                    ],
                    "additionalProperties": False
                }
            }
        },
        "required": ["questions"],
        "additionalProperties": False
    }
