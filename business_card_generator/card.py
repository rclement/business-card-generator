import io
import mimetypes

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from segno import QRCode, helpers


class CardKind(str, Enum):
    mecard = "mecard"


class CardFormat(str, Enum):
    svg = "svg"
    png = "png"


class CardParams(BaseModel):
    name: str
    nickname: Optional[str] = None
    title: Optional[str] = None
    birthday: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    kind: CardKind = CardKind.mecard
    format: CardFormat = CardFormat.svg
    scale: float = 4.0


@dataclass
class Card:
    image: io.BytesIO
    mimetype: str


def create_mecard(params: CardParams) -> QRCode:
    return helpers.make_mecard(
        name=params.name,
        nickname=params.nickname,
        memo=params.title,
        birthday=params.birthday.strftime("%Y%m%d") if params.birthday else None,
        email=params.email,
        phone=params.phone,
        houseno=params.street,
        city=params.city,
        zipcode=params.zipcode,
        prefecture=params.state,
        country=params.country,
    )


def create_card(params: CardParams) -> Card:
    factories = {
        CardKind.mecard: create_mecard,
    }
    qrcode = factories[params.kind](params)

    image = io.BytesIO()
    qrcode.save(image, kind=params.format.value, scale=params.scale)
    image.seek(0)
    mimetype = mimetypes.types_map[f".{params.format.value}"]

    return Card(image=image, mimetype=mimetype)
