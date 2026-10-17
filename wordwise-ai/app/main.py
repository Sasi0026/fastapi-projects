from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.schemas import Context, WordResponse
from app.services.word_service import get_word_info

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="WordWise AI")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/word/{term}")
def get_word(term: str, context: Context = Context.general):
    try:
        result = get_word_info(term, context)
        return result
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"LLM error: {e}")
    
