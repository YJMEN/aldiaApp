import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def _as_bool(value):
    return str(value).lower() in ("1", "true", "yes")


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-me"
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    DATABASE_PATH = os.path.join(PROJECT_ROOT, "app", "aldiaapp.db")
    MONTHLY_FEE = int(os.environ.get("MONTHLY_FEE", 12000))
    ENABLE_SCHEDULER = _as_bool(os.environ.get("ENABLE_SCHEDULER", "0"))
    FLASK_DEBUG = _as_bool(os.environ.get("FLASK_DEBUG", "0"))
    PORT = int(os.environ.get("PORT", 5001))


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
