from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from .card import CardParams, create_card


router = APIRouter()


@router.get(
    "/card",
    summary="Generate business card",
    description="Generate business card",
)
def get_card(params: CardParams = Depends()) -> StreamingResponse:
    card = create_card(params)
    return StreamingResponse(content=card.image, media_type=card.mimetype)
