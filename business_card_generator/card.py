from datetime import date
from io import BytesIO, StringIO
from typing import Optional
from pydantic import BaseModel, EmailStr
from segno import QRCode, helpers, make_qr


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


class BaseCard:
    params: CardParams
    data: str
    qrcode: QRCode
    name: str = "card"

    def __init__(self, params: CardParams) -> None:
        self.params = params
        self.data = self.generate_data(params)
        self.qrcode = make_qr(self.data)

    def generate_data(self, params: CardParams) -> str:
        raise NotImplementedError  # pragma: no cover

    def vcf(self) -> StringIO:
        return StringIO(self.data)

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
            name=params.name,
            displayname=params.name,
            email=params.email,
            phone=params.phone,
            memo=params.title,
            nickname=params.nickname,
            birthday=params.birthday,
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
