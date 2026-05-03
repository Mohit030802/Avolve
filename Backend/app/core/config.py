import yaml
import os
from pathlib import Path
from typing import Any, Dict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Avolve Backend"
    API_V1_STR: str = "/api/v1"
    
    # Secrets will be loaded into this dictionary
    secrets: Dict[str, Any] = {}

    def load_secrets(self):
        secrets_path = Path(__file__).parent.parent.parent / "secrets" / "secrets.yml"
        if secrets_path.exists():
            with open(secrets_path, "r") as f:
                self.secrets = yaml.safe_load(f) or {}
        else:
            print(f"Warning: Secrets file not found at {secrets_path}")

    @property
    def secret_key(self) -> str:
        return self.secrets.get("app", {}).get("secret_key", "fallback_temporary_dev_key")

    @property
    def algorithm(self) -> str:
        return self.secrets.get("app", {}).get("algorithm", "HS256")

    @property
    def access_token_expire_minutes(self) -> int:
        return self.secrets.get("app", {}).get("access_token_expire_minutes", 30)

    @property
    def google_api_key(self) -> str:
        return self.secrets.get("app", {}).get("google_api_key", "")

    @property
    def hf_token(self) -> str:
        return self.secrets.get("app", {}).get("HF_TOKEN", "")

    @property
    def db_user(self) -> str:
        return self.secrets.get("app", {}).get("db_user", "postgres")

    @property
    def db_password(self) -> str:
        return self.secrets.get("app", {}).get("db_password", "")

    @property
    def db_host(self) -> str:
        return self.secrets.get("app", {}).get("db_host", "localhost")

    @property
    def db_port(self) -> int:
        return self.secrets.get("app", {}).get("db_port", 5432)

    @property
    def db_name(self) -> str:
        return self.secrets.get("app", {}).get("db_name", "Avolve")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def langchain_api_key(self) -> str:
        return self.secrets.get("app", {}).get("langchain_api_key", "")

    @property
    def langchain_project(self) -> str:
        return self.secrets.get("app", {}).get("langchain_project", "Avolve-Agents")

    @property
    def hf_hub_disable_symlinks_warning(self) -> str:
        return "1"

    @property
    def logs_dir(self) -> Path:
        path = Path(__file__).parent.parent.parent / "logs"
        path.mkdir(parents=True, exist_ok=True)
        return path

settings = Settings()
settings.load_secrets()
