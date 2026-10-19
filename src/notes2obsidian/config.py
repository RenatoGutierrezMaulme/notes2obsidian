from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ROOT / ".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )

    telegram_bot_token : SecretStr
    telegram_bot_username : SecretStr

    def telegram_bot_token(self):
        return self.telegram_bot_token
    def telegram_bot_username(self):
        return self.telegram_bot_username


