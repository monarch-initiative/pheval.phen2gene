from pathlib import Path

from phenopackets import PhenotypicFeature
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


def write_hpo_ids_to_output_file(
    output_file: Path, phenotypic_profile: [PhenotypicFeature]
) -> None:
    """Write a list of HPO ids to a new text file for input into Phen2Gene."""
    with open(output_file, "w") as output:
        output.write("\n".join([hpo.type.id for hpo in phenotypic_profile]))
    output.close()


def prepare_input(output_dir: Path, phenopacket_path: Path) -> None:
    """Prepare a text file input for Phen2Gene from a phenopacket."""
    output_dir.mkdir(exist_ok=True)
    phenopacket = phenopacket_reader(phenopacket_path)
    phenotypic_profile = PhenopacketUtil(phenopacket).observed_phenotypic_features()
    output_file_path = output_dir.joinpath(phenopacket_path.name + ".txt")
    write_hpo_ids_to_output_file(output_file_path, phenotypic_profile)


def prepare_inputs(output_dir: Path, phenopacket_dir: Path) -> None:
    """Prepare text files input for Phen2Gene from a directory of phenopackets."""
    for phenopacket_path in all_files(phenopacket_dir):
        prepare_input(output_dir, phenopacket_path)

@click.command("prepare-inputs")
@click.option(
    "--phenopacket-dir",
    "-p",
    metavar="Path",
    required=True,
    help="Path to phenopacket directory.",
    type=Path,
)
@click.option(
    "--output-dir",
    "-o",
    metavar="Path",
    required=True,
    help="Path to output directory.",
    type=Path,
)
def prepare_inputs_command(phenopacket_dir: Path, output_dir: Path):
    prepare_inputs(output_dir=output_dir, phenopacket_dir=phenopacket_dir)