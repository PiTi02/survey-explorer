from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Kluczowe zmienne środowiskowe
    PATH_DATA: str
    FILE_NAME: str

    # Ustawienie ścieżki do .env
    model_config = SettingsConfigDict(
        env_file='config/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

# Inicjalizacja ustawień globalnie
settings = Settings()
