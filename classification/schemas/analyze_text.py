from  pydantic import BaseModel



class AnalyzeTextRes(BaseModel):
    language: str
    entities: {
        persons: List[str]
    }
