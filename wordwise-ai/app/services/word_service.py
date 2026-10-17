import os 
from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.schemas import Context, WordResponse


# word_service.py -> services -> app -> wordwise-ai -> fastapi-projects
load_dotenv(Path(__file__).resolve().parents[3] / ".env")


llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)



parser = PydanticOutputParser(pydantic_object = WordResponse)

# What each context means, so the LLM knows the learner's world
CONTEXT_DESCRIPTIONS = {
    Context.general: "everyday life (home, friends, shopping, travel)",
    Context.student: "a student (school or college: assignments, exams, classes, projects)",
    Context.corporate: "a corporate professional (meetings, clients, managers, project timelines)",
    Context.tech: "a software or tech professional (code, deployments, AI models, releases)",
}

prompt = ChatPromptTemplate.from_template(
   """
Explain the following word for an English learner.

Word: {term}
Learner's context: {context}

Include:
1. A simple, clear definition.
2. The part of speech.
3. How the word is used in the learner's context.
4. Verb forms, if applicable.
5. Three example sentences set in the learner's context.
6. Useful synonyms and antonyms.
7. Common word combinations (collocations).

Use simple English and make the explanation easy to understand.

{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

def get_word_info(term: str, context: Context = Context.general) -> WordResponse:
    result = chain.invoke({"term": term, "context": CONTEXT_DESCRIPTIONS[context]})
    return result


