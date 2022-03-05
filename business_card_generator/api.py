import mimetypes
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from .card import CardParams, MeCard, VCard


router = APIRouter()


@router.get(
    "/vcard.svg",
    summary="Generate vCard SVG",
    description="Generate vCard QR Code in SVG format",
    tags=["vcard"],
)
def get_vcard_svg(params: CardParams = Depends()) -> StreamingResponse:
    vcard = VCard(params)
    return StreamingResponse(
        content=vcard.qrcode_svg(),
        media_type=mimetypes.types_map[".svg"],
        headers={"Content-Disposition": "filename=vcard.svg"},
    )


@router.get(
    "/vcard.png",
    summary="Generate vCard PNG",
    description="Generate vCard QR Code in PNG format",
    tags=["vcard"],
)
def get_vcard_png(params: CardParams = Depends()) -> StreamingResponse:
    vcard = VCard(params)
    return StreamingResponse(
        content=vcard.qrcode_png(),
        media_type=mimetypes.types_map[".png"],
        headers={"Content-Disposition": "filename=vcard.png"},
    )


@router.get(
    "/vcard.vcf",
    summary="Generate vCard VCF",
    description="Generate vCard in VCF format",
    tags=["vcard"],
)
def get_vcard_vcf(params: CardParams = Depends()) -> StreamingResponse:
    vcard = VCard(params)
    return StreamingResponse(
        content=vcard.vcf(),
        media_type=mimetypes.types_map[".vcf"],
        headers={"Content-Disposition": "filename=vcard.vcf"},
    )


@router.get(
    "/mecard.svg",
    summary="Generate MeCard SVG",
    description="Generate MeCard QR Code in SVG format",
    tags=["mecard"],
)
def get_mecard_svg(params: CardParams = Depends()) -> StreamingResponse:
    mecard = MeCard(params)
    return StreamingResponse(
        content=mecard.qrcode_svg(),
        media_type=mimetypes.types_map[".svg"],
        headers={"Content-Disposition": "filename=mecard.svg"},
    )


@router.get(
    "/mecard.png",
    summary="Generate MeCard PNG",
    description="Generate MeCard QR Code in PNG format",
    tags=["mecard"],
)
def get_mecard_png(params: CardParams = Depends()) -> StreamingResponse:
    mecard = MeCard(params)
    return StreamingResponse(
        content=mecard.qrcode_png(),
        media_type=mimetypes.types_map[".png"],
        headers={"Content-Disposition": "filename=mecard.png"},
    )


@router.get(
    "/mecard.vcf",
    summary="Generate MeCard VCF",
    description="Generate MeCard in VCF format",
    tags=["mecard"],
)
def get_mecard_vcf(params: CardParams = Depends()) -> StreamingResponse:
    mecard = MeCard(params)
    return StreamingResponse(
        content=mecard.vcf(),
        media_type=mimetypes.types_map[".vcf"],
        headers={"Content-Disposition": "filename=mecard.vcf"},
    )
