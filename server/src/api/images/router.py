from fastapi import APIRouter, Depends, Body
from .service import ImageTextService
from .types import SearchDocuments

router = APIRouter(
    prefix="/images",
    tags=["images"],
)

def get_image_text_service():
    return ImageTextService()

@router.get('/text')
async def get_images_texts(image_text_service: ImageTextService = Depends(get_image_text_service)):
    return image_text_service.get_texts()


@router.post('/results')
async def get_results(search_documents: SearchDocuments = Body(...), 
                      image_text_service: ImageTextService = Depends(get_image_text_service)):
    return image_text_service.get_results(search_documents.data)