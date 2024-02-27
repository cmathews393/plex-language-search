import rtoml
import os
from typing import Dict, Any

config_file = "config.toml"


def ensure_config_exists() -> None:
    """Ensure the configuration file exists, and create it with default values if it doesn't."""
    if not os.path.exists(config_file):
        print("Config file missing!")
        print("Current Working Directory:", os.getcwd())
        with open(config_file, "w") as file:
            rtoml.dump({}, file)


def read_config(service: str) -> Dict[str, Any]:
    """Read config from file."""
    print("Reading config...")
    ensure_config_exists()
    with open(config_file, "r") as file:
        config = rtoml.load(file)
    return config.get(service, {})


def write_config(service: str, data: Dict[str, Any]) -> None:
    """Write file (not used in all implementations)."""
    print("Writing config...")
    ensure_config_exists()
    with open(config_file, "r") as file:
        config = rtoml.load(file)
    config[service] = data
    with open(config_file, "w") as file:
        rtoml.dump(config, file)
