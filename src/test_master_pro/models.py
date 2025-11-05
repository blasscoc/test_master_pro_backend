from pydantic import BaseModel
from typing import List

class GenerateRequest(BaseModel):
    teks_codes: List[str]  # e.g. ["3.5(A)", "3.5(B)"]

class GenerateResponse(BaseModel):
    markdown: str
