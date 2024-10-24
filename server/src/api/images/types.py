from pydantic import BaseModel

class ChromaResponse(BaseModel):
    ids: list[str]
    documents: list[str]

class Document(BaseModel):
    id: str | None
    document: str | None
    semantic: float
    
class SearchParameters(BaseModel):
    modality: str
    documents: list[Document]

class SearchDocuments(BaseModel):
    data: SearchParameters

class Documents(BaseModel):
    data: list[Document]