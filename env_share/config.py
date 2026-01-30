import json
import os
from dataclasses import dataclass, field
from typing import Self

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


CONFIG_FILE = "dxsync.json"
PYPROJECT_FILE = "pyproject.toml"


@dataclass
class Config:
    envs: list[str] = field(default_factory=lambda: ["dev", "stg", "prd"])
    env_dir: str = ".env"
    enc_dir: str = "enc"
    work_dir: str = "tmp/dxsync"
    encrypted_prefix: str = "encrypted:"

    @classmethod
    def load(cls) -> Self:
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls._from_dict(data)

        if os.path.isfile(PYPROJECT_FILE):
            with open(PYPROJECT_FILE, "rb") as f:
                pyproject = tomllib.load(f)
            if "tool" in pyproject and "dxsync" in pyproject["tool"]:
                return cls._from_dict(pyproject["tool"]["dxsync"])

        return cls()

    @classmethod
    def _from_dict(cls, data: dict) -> Self:
        return cls(
            envs=data.get("envs", ["dev", "stg", "prd"]),
            env_dir=data.get("env_dir", ".env"),
            enc_dir=data.get("enc_dir", "enc"),
            work_dir=data.get("work_dir", "tmp/dxsync"),
            encrypted_prefix=data.get("encrypted_prefix", "encrypted:"),
        )

    @property
    def latest_dir(self) -> str:
        return os.path.join(self.env_dir, "latest")

    @property
    def keys_dir(self) -> str:
        return os.path.join(self.env_dir, "keys")

    @property
    def gitignore_required(self) -> list[str]:
        return [f"{self.env_dir}/*", f"{self.work_dir}/*", "*.keys"]


_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def reload_config() -> Config:
    global _config
    _config = Config.load()
    return _config


GITIGNORE_PATH = ".gitignore"
