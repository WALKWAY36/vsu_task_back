from pydantic import BaseModel


class DtoFuzzy(BaseModel):
    matched: str
    suggestion: str
    score: float
