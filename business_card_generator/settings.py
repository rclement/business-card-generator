from pydantic import BaseSettings

from . import __about__


class Settings(BaseSettings):
    app_name: str = __about__.__name__
    app_description: str = __about__.__description__
    app_version: str = __about__.__version__
    app_environment: str = "production"

    force_https: bool = False
