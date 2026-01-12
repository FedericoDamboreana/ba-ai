from typing import Dict, Any, List, Optional
from app.models.project import Project
from app.models.documentation_item import DocumentationItem
from app.models.question import Question


def get_system_prompt(doc_type: str) -> str:
    """
    Get the system prompt based on documentation type.

    Args:
        doc_type: Type of documentation (PRD, Epic, UserStory, FRS)

    Returns:
        System prompt string
    """
    base_prompt = """You are a senior Business Analyst creating professional documentation.
Maintain a formal, professional tone suitable for German business clients.
Use clear, precise language and follow industry-standard formats."""

    type_specific = {
        "UserStory": """
For User Stories:
- Use the standard format: "As a [user type], I want [goal], so that [benefit]"
- Write Acceptance Criteria in BDD/Gherkin format (Given/When/Then)
- Include multiple scenarios: happy path, edge cases, and error cases
- Be specific and testable in acceptance criteria
- Consider both functional and non-functional requirements""",

        "PRD": """
For Product Requirements Documents:
- Structure with clear sections: Overview, Objectives, Scope, Stakeholders, Requirements, Constraints
- Define success criteria and metrics
- Identify assumptions and dependencies
- Use numbered requirements for easy reference
- Distinguish between must-have and nice-to-have features""",

        "Epic": """
For Epic Documentation:
- Define the business value and user problems being solved
- Outline scope boundaries (what's in and what's out)
- List high-level features and capabilities
- Identify dependencies on other epics or systems
- Include success metrics and acceptance criteria for the epic as a whole""",

        "FRS": """
For Functional Requirements Specification:
- Organize requirements by functional area or module
- Use clear requirement IDs (e.g., FR-001, FR-002)
- Specify inputs, outputs, and processing logic
- Define business rules and validation criteria
- Include error handling and edge cases
- Prioritize requirements (Must/Should/Could)"""
    }

    return base_prompt + type_specific.get(doc_type, "")


def get_user_prompt(
    project: Project,
    item: DocumentationItem,
    questions: List[Question],
    feedback: Optional[str] = None
) -> str:
    """
    Build the user prompt with all context.

    Args:
        project: The project
        item: The documentation item
        questions: List of answered questions
        feedback: Optional regeneration feedback

    Returns:
        Formatted user prompt
    """
    # Format Q&A pairs
    qa_pairs = []
    for i, q in enumerate(questions, 1):
        answer = q.answer if q.is_answered else "Not answered"
        qa_pairs.append(f"{i}. Q: {q.question_text}\n   A: {answer}")

    qa_text = "\n\n".join(qa_pairs)

    prompt = f"""Create {item.type.value} documentation based on the following information.

**Project Context:**
- Project: {project.name}
- Client: {project.client or "Not specified"}
- Description: {project.description}

**Project Knowledge Base:**
{project.knowledge_base if project.knowledge_base else "No prior context."}

**Documentation Item:**
- Title: {item.title}
- Description: {item.description}

**Questions and Answers:**
{qa_text}
"""

    if feedback:
        prompt += f"""

**Regeneration Feedback:**
The user provided the following feedback on the previous version:
{feedback}

Please incorporate this feedback into the new version."""

    return prompt


def get_user_story_schema() -> Dict[str, Any]:
    """Get JSON schema for User Story response."""
    return {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Clear, concise title for the user story"
            },
            "user_story": {
                "type": "object",
                "properties": {
                    "as_a": {"type": "string", "description": "User role or persona"},
                    "i_want": {"type": "string", "description": "The feature or capability"},
                    "so_that": {"type": "string", "description": "The benefit or value"}
                },
                "required": ["as_a", "i_want", "so_that"],
                "additionalProperties": False
            },
            "acceptance_criteria": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "scenario_name": {"type": "string"},
                        "given": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Preconditions"
                        },
                        "when": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Actions"
                        },
                        "then": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Expected outcomes"
                        }
                    },
                    "required": ["scenario_name", "given", "when", "then"],
                    "additionalProperties": False
                }
            },
            "notes": {
                "type": ["string", "null"],
                "description": "Additional notes or clarifications"
            },
            "dependencies": {
                "type": ["array", "null"],
                "items": {"type": "string"},
                "description": "Dependencies on other stories or systems"
            }
        },
        "required": ["title", "user_story", "acceptance_criteria"],
        "additionalProperties": False
    }


def get_prd_schema() -> Dict[str, Any]:
    """Get JSON schema for PRD response."""
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "overview": {"type": "string", "description": "High-level project overview"},
            "objectives": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Project objectives"
            },
            "scope": {
                "type": "object",
                "properties": {
                    "in_scope": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "out_of_scope": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["in_scope", "out_of_scope"],
                "additionalProperties": False
            },
            "stakeholders": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string"},
                        "responsibilities": {"type": "string"}
                    },
                    "required": ["role", "responsibilities"],
                    "additionalProperties": False
                }
            },
            "requirements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "description": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["Must Have", "Should Have", "Could Have"]
                        }
                    },
                    "required": ["id", "description", "priority"],
                    "additionalProperties": False
                }
            },
            "constraints": {
                "type": "array",
                "items": {"type": "string"}
            },
            "success_criteria": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["title", "overview", "objectives", "scope", "requirements"],
        "additionalProperties": False
    }


def get_epic_schema() -> Dict[str, Any]:
    """Get JSON schema for Epic response."""
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "business_value": {
                "type": "string",
                "description": "Why this epic matters"
            },
            "user_problems": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Problems this epic solves"
            },
            "scope": {
                "type": "object",
                "properties": {
                    "included": {"type": "array", "items": {"type": "string"}},
                    "excluded": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["included", "excluded"],
                "additionalProperties": False
            },
            "features": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["name", "description"],
                    "additionalProperties": False
                }
            },
            "dependencies": {
                "type": "array",
                "items": {"type": "string"}
            },
            "success_metrics": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["title", "business_value", "user_problems", "scope", "features"],
        "additionalProperties": False
    }


def get_frs_schema() -> Dict[str, Any]:
    """Get JSON schema for FRS response."""
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "overview": {"type": "string"},
            "functional_areas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "area_name": {"type": "string"},
                        "requirements": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "description": {"type": "string"},
                                    "priority": {
                                        "type": "string",
                                        "enum": ["Must", "Should", "Could"]
                                    },
                                    "inputs": {"type": ["string", "null"]},
                                    "outputs": {"type": ["string", "null"]},
                                    "business_rules": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["id", "description", "priority"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["area_name", "requirements"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["title", "overview", "functional_areas"],
        "additionalProperties": False
    }


def get_response_schema(doc_type: str) -> Dict[str, Any]:
    """
    Get the appropriate response schema based on doc type.

    Args:
        doc_type: Documentation type

    Returns:
        JSON schema dictionary
    """
    schemas = {
        "UserStory": get_user_story_schema(),
        "PRD": get_prd_schema(),
        "Epic": get_epic_schema(),
        "FRS": get_frs_schema()
    }

    return schemas.get(doc_type, get_user_story_schema())
