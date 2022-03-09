from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse


router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@router.get("/", response_class=_TemplateResponse, include_in_schema=False)
def get_home(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("home.html", dict(request=request))


@router.get("/card", include_in_schema=False)
def get_card(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("card.html", dict(request=request))
