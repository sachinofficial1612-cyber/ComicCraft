from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=1000)
    character_name: str = Field(default="Alex", max_length=80)
    setting: str = Field(default="enchanted forest", max_length=120)
    tone: str = Field(default="dramatic", max_length=50)
    art_style: str = Field(default="comic book", max_length=80)
