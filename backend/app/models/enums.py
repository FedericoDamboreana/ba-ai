import enum

class ProjectStatus(enum.Enum):
    ACTIVE = "Active"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"

class DocumentationItemStatus(enum.Enum):
    DRAFT = "Draft"
    IN_PROGRESS = "InProgress"
    QUESTIONS_COMPLETE = "QuestionsComplete"
    GENERATED = "Generated"

class DocumentationType(enum.Enum):
    PRD = "PRD"
    EPIC = "Epic"
    USER_STORY = "UserStory"
    FRS = "FRS"

class QuestionType(enum.Enum):
    TEXT = "Text"
    MULTIPLE_CHOICE = "MultipleChoice"
    CHECKBOX = "Checkbox"
