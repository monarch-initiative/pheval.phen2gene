from dataclasses import dataclass
from pathlib import Path

import yaml
from serde import serde
from serde.yaml import from_yaml


@serde
@dataclass
class Phen2GeneRun:
    environment: str
    path_to_phen2gene_software_directory: Path


@serde
@dataclass
class Phen2GeneConfig:
    run: Phen2GeneRun


def parse_phen2gene_config(config_path: Path) -> Phen2GeneConfig:
    """Reads the config file."""
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    config_file.close()
    return from_yaml(Phen2GeneConfig, yaml.dump(config))
