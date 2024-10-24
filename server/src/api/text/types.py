from pydantic import BaseModel

class ChromaResponse(BaseModel):
    ids: list[str]
    documents: list[str]

class Document(BaseModel):
    id: str | None
    document: str | None
    semantic: float

class Documents(BaseModel):
    data: list[Document]