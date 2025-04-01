from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    APP_AUTHOR: str

    File_Allowed_Types: list[str]
    File_Max_Size: int
    File_Chunk_Size: int

    class Config():
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    return Settings()
