from pathlib import Path
from typing import List

from phenopackets import PhenotypicFeature
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


def write_hpo_ids_to_output_file(
    output_file: Path, phenotypic_profile: List[PhenotypicFeature]
) -> None:
    """
    Write a list of HPO ids to a new text file for input into Phen2Gene.
    Args:
        output_file (Path): Path to the file to write text file containing HPO ids.
        phenotypic_profile (List[PhenotypicFeature]): List of phenotypic features.
    """
    with open(output_file, "w") as output:
        output.write("\n".join([hpo.type.id for hpo in phenotypic_profile]))
    output.close()


def prepare_input(output_dir: Path, phenopacket_path: Path) -> None:
    """
    Prepare a text file input for Phen2Gene from a phenopacket.
    Args:
        output_dir (Path): Path to the output directory to write text file.
        phenopacket_path (Path): Path to the phenopacket file.
    """
    output_dir.mkdir(exist_ok=True)
    phenopacket = phenopacket_reader(phenopacket_path)
    phenotypic_profile = PhenopacketUtil(phenopacket).observed_phenotypic_features()
    output_file_path = output_dir.joinpath(phenopacket_path.name + ".txt")
    write_hpo_ids_to_output_file(output_file_path, phenotypic_profile)


def prepare_inputs(output_dir: Path, phenopacket_dir: Path) -> None:
    """
    Prepare text files input for Phen2Gene from a directory of phenopackets.
    Args:
        output_dir (Path): Path to the output directory to write text files.
        phenopacket_dir (Path): Path to the phenopacket directory.
    """
    for phenopacket_path in all_files(phenopacket_dir):
        prepare_input(output_dir, phenopacket_path)
