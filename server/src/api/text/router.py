from fastapi import APIRouter, Depends
from fastapi.params import Body
from .service import TextService
from .types import ChromaResponse, Documents

router = APIRouter(
    prefix="/text",
    tags=["text"],
)

def get_text_service():
    return TextService()

@router.get('/category')
async def get_categories(text_service: TextService=Depends(get_text_service)) -> ChromaResponse:
    return text_service.get_categories()


@router.get('')
async def get_docs(text_service: TextService=Depends(get_text_service), category: str = '') -> ChromaResponse:
   return text_service.get_docs(category)


@router.post('/similar')
async def get_similar(selected_docs: Documents = Body(...), text_service: TextService = Depends(get_text_service)) -> ChromaResponse:
    return text_service.get_similar(selected_docs.data)


