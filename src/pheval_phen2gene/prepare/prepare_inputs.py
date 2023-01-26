from pathlib import Path
from typing import List

from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


def extract_proband_hpo_ids(phenopacket_path: Path) -> List[str]:
    """Extract a list of HPO ids used to describe the proband's phenotypic profile in a phenopacket."""
    phenopacket = phenopacket_reader(phenopacket_path)
    phenotypic_profile = PhenopacketUtil(phenopacket).observed_phenotypic_features()
    hpo_ids = [hpo.type.id for hpo in phenotypic_profile]
    return hpo_ids


def write_hpo_ids_to_input_file(output_file: Path, hpo_ids: List[str]) -> None:
    """Write a list of HPO ids to a new text file for input into Phen2Gene."""
    with open(output_file, "w") as output:
        output.write("\n".join(hpo_ids))
    output.close()


def prepare_input(output_dir: Path, phenopacket_path: Path) -> None:
    """Prepare the text file input for Phen2Gene."""
    hpo_ids = extract_proband_hpo_ids(phenopacket_path)
    output_file_path = output_dir.joinpath(phenopacket_path.name + ".txt")
    write_hpo_ids_to_input_file(output_file_path, hpo_ids)
