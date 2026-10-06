from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str = ""
    hf_api_key: str = ""
    gemini_text_model: str = "gemini-2.0-flash"
    gemini_story_model: str = "gemini-2.0-flash"
    image_device: str = "auto"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
