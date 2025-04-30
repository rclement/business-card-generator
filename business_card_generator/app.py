import mimetypes

from http import HTTPStatus
from typing import Optional
from flask import Blueprint, Flask, abort, redirect, render_template, request, send_file
from pydantic import ValidationError
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.wrappers import Response
from whitenoise import WhiteNoise

from . import __about__
from .card import CardParams, MeCard, VCard
from .settings import Settings


# ------------------------------------------------------------------------------


views_bp = Blueprint("views", __name__)


def card_params_from_args() -> CardParams:
    try:
        return CardParams(**request.args.to_dict())
    except ValidationError:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY)


@views_bp.get("/")
def get_home() -> str:
    return render_template("home.html")


@views_bp.get("/card")
def get_card() -> str:
    return render_template("card.html")


@views_bp.get("/vcard.svg")
def get_vcard_svg() -> Response:
    card_params = card_params_from_args()
    vcard = VCard(card_params)
    return send_file(
        vcard.qrcode_svg(),
        mimetype=mimetypes.types_map[".svg"],
        download_name="vcard.svg",
    )


@views_bp.get("/vcard.png")
def get_vcard_png() -> Response:
    card_params = card_params_from_args()
    vcard = VCard(card_params)
    return send_file(
        vcard.qrcode_png(),
        mimetype=mimetypes.types_map[".png"],
        download_name="vcard.png",
    )


@views_bp.get("/vcard.vcf")
def get_vcard_vcf() -> Response:
    card_params = card_params_from_args()
    vcard = VCard(card_params)
    return send_file(
        vcard.vcf(),
        mimetype=mimetypes.types_map[".vcf"],
        download_name="vcard.vcf",
    )


@views_bp.get("/mecard.svg")
def get_mecard_svg() -> Response:
    card_params = card_params_from_args()
    mecard = MeCard(card_params)
    return send_file(
        mecard.qrcode_svg(),
        mimetype=mimetypes.types_map[".svg"],
        download_name="mecard.svg",
    )


@views_bp.get("/mecard.png")
def get_mecard_png() -> Response:
    card_params = card_params_from_args()
    mecard = MeCard(card_params)
    return send_file(
        mecard.qrcode_png(),
        mimetype=mimetypes.types_map[".png"],
        download_name="mecard.png",
    )


@views_bp.get("/mecard.vcf")
def get_mecard_vcf() -> Response:
    card_params = card_params_from_args()
    mecard = MeCard(card_params)
    return send_file(
        mecard.vcf(),
        mimetype=mimetypes.types_map[".vcf"],
        download_name="mecard.vcf",
    )


# ------------------------------------------------------------------------------


def create_app(env_file: Optional[str] = ".env") -> Flask:
    settings = Settings(_env_file=env_file)

    app = Flask(__name__)
    app.config.from_object(settings)
    app.config["about"] = dict(
        name=__about__.__name__,
        description=__about__.__description__,
        version=__about__.__version__,
    )
    app.debug = settings.app_environment == "development"
    app.testing = settings.app_environment == "testing"

    app.wsgi_app = WhiteNoise(  # type: ignore[method-assign]
        app.wsgi_app,
        root=app.static_folder,
        prefix=app.static_url_path,
        autorefresh=app.debug,
    )
    app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
        app.wsgi_app, x_proto=1, x_host=1
    )

    @app.before_request
    def _force_https() -> Optional[Response]:
        if settings.force_https and request.url.startswith("http://"):
            https_url = request.url.replace("http://", "https://", 1)
            return redirect(https_url)
        return None

    app.register_blueprint(views_bp, url_prefix="")

    return app
