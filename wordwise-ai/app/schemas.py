from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Context(str, Enum):
    general = "general"
    student = "student"
    corporate = "corporate"
    tech = "tech"


class VerbForms(BaseModel):
    base: str
    past: str
    past_participle: str
    present_participle: str
    third_person: str


class WordResponse(BaseModel):
    word: str
    pronunciation: str
    part_of_speech: str
    definition: str
    context_meaning: str = Field(description="How this word is used in the learner's context")
    verb_forms: Optional[VerbForms] = None
    examples: List[str] = Field(description="Three example sentences set in the learner's context")
    synonyms: List[str]
    antonyms: List[str]
    collocations: List[str]
    professional_usage: str
    common_mistakes: List[str]
