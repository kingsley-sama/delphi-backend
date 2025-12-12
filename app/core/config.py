from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    APP_NAME:str = "Delphi"
    DEBUG:bool = False
    DATABASE_URL:str
    PORT:int = 3000
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
        
    )

settings = Settings()

print(settings.model_dump())