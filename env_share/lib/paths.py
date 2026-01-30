import os
from dataclasses import dataclass
from env_share.config import get_config
from env_share.lib.io_utils import ensure_dirs


@dataclass(frozen=True)
class EnvPaths:
    enc: str
    plain: str
    latest: str
    work: str
    key: str


def prepare_paths(target_env: str) -> EnvPaths:
    cfg = get_config()
    ensure_dirs([cfg.env_dir, cfg.work_dir, cfg.latest_dir, cfg.enc_dir, cfg.keys_dir])
    return EnvPaths(
        enc=os.path.join(cfg.enc_dir, f".env.{target_env}.enc"),
        plain=os.path.join(cfg.env_dir, target_env),
        latest=os.path.join(cfg.latest_dir, f".env.{target_env}"),
        work=os.path.join(cfg.work_dir, f".env.{target_env}.enc"),
        key=os.path.join(cfg.keys_dir, f"{target_env}.keys"),
    )
