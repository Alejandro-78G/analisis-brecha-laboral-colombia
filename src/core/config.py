from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración global del sistema con validación Pydantic v2.
    Lee automáticamente las variables de entorno del archivo .env.
    """
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Directorios de datos
    DATA_RAW_PATH: Path = Path("./data/raw")
    DATA_PROCESSED_PATH: Path = Path("./data/processed")
    DUCKDB_PATH: Path = Path("./data/brecha_laboral.duckdb")

    # APIs Oficiales
    DATOS_GOV_APP_TOKEN: str | None = None
    DATOS_GOV_SPE_DATASET_ID: str = "vacantes-spe"

    # Scraping Engine
    SCRAPER_CONCURRENCY: int = 5
    SCRAPER_TIMEOUT: int = 15
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
