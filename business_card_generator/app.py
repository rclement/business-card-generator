from typing import Optional
from fastapi import FastAPI

from . import __about__


def create_app(env_file: Optional[str] = ".env") -> FastAPI:
    from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
    from fastapi.middleware.cors import CORSMiddleware
    from . import api, views
    from .settings import Settings

    settings = Settings(_env_file=env_file)  # type: ignore

    app = FastAPI(
        title=__about__.__name__,
        description=__about__.__description__,
        version=__about__.__version__,
    )
    app.state.settings = settings

    if settings.force_https:
        app.add_middleware(HTTPSRedirectMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(views.router, prefix="")
    app.include_router(api.router, prefix="/api")

    return app
