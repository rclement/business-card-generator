from datetime import date
from io import BytesIO
from typing import Any, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator
from segno import QRCode, helpers, make_qr


class CardParams(BaseModel):
    firstname: str
    lastname: str
    nickname: Optional[str] = None
    birthday: Optional[date] = None
    company: Optional[str] = None
    job: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    picture: Optional[HttpUrl] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

    @field_validator("birthday", "email", "website", "picture", mode="before")
    @classmethod
    def validate_empty(cls, value: Optional[str]) -> Optional[str]:
        return value or None


class BaseCard:
    params: CardParams
    data: str
    qrcode: QRCode
    name: str = "card"

    def __init__(self, params: CardParams) -> None:
        self.params = params
        self.data = self.generate_data(params)
        self.qrcode = make_qr(self.data, encoding="utf-8")

    def generate_data(self, params: CardParams) -> str:
        raise NotImplementedError  # pragma: no cover

    def vcf(self) -> BytesIO:
        return BytesIO(self.data.encode("utf-8"))

    def qrcode_svg(self, scale: float = 4.0) -> BytesIO:
        image = BytesIO()
        self.qrcode.save(image, kind="svg", scale=scale, svgclass=self.name)
        image.seek(0)
        return image

    def qrcode_png(self, scale: float = 4.0) -> BytesIO:
        image = BytesIO()
        self.qrcode.save(image, kind="png", scale=scale)
        image.seek(0)
        return image


class VCard(BaseCard):
    name: str = "vcard"

    def __init__(self, params: CardParams) -> None:
        super().__init__(params)

    def generate_data(self, params: CardParams) -> str:
        return helpers.make_vcard_data(
            name=f"{params.lastname};{params.firstname}",
            displayname=f"{params.firstname} {params.lastname}",
            nickname=params.nickname,
            birthday=params.birthday,
            org=params.company,
            title=params.job,
            email=params.email,
            phone=params.phone,
            url=str(params.website) if params.website else None,
            photo_uri=str(params.picture) if params.picture else None,
            street=params.street,
            city=params.city,
            region=params.state,
            zipcode=params.zipcode,
            country=params.country,
        )


class MeCard(BaseCard):
    name: str = "mecard"

    def __init__(self, params: CardParams) -> None:
        super().__init__(params)

    def generate_data(self, params: CardParams) -> str:
        return helpers.make_mecard_data(
            name=f"{params.lastname},{params.firstname}",
            nickname=params.nickname,
            birthday=params.birthday.strftime("%Y%m%d") if params.birthday else None,
            memo=params.company,
            email=params.email,
            phone=params.phone,
            url=str(params.website) if params.website else None,
            houseno=params.street,
            city=params.city,
            zipcode=params.zipcode,
            prefecture=params.state,
            country=params.country,
        )
