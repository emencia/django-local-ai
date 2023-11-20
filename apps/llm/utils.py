from typing import Any, Dict
import os
import yaml


def load_models_conf(config_path: str) -> Dict[str, Any]:
    config_dict = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as stream:
            try:
                config_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print(f"File {config_path} does not exist: can not load models config")
    return config_dict
