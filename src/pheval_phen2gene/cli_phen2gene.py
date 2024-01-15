from pathlib import Path

import click
from pheval.prepare.custom_exceptions import MutuallyExclusiveOptionError

from pheval_phen2gene.prepare.prepare_commands import prepare_commands
from pheval_phen2gene.prepare.prepare_inputs import prepare_inputs


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
    """
    Prepare input for Phen2Gene from a phenopacket directory.
    Args:
        phenopacket_dir (Path): Path to the phenopacket directory.
        output_dir (Path): Path to the directory to write the input txt files.
    """
    prepare_inputs(output_dir=output_dir, phenopacket_dir=phenopacket_dir)


@click.command("prepare-commands")
@click.option(
    "--environment",
    "-e",
    required=False,
    default="local",
    show_default=True,
    help="Environment to run commands.",
    type=click.Choice(["local", "docker"]),
)
@click.option(
    "--file-prefix",
    "-f",
    required=True,
    metavar=str,
    type=str,
    help="Prefix for output batch file.",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    type=Path,
    help="Directory for batch file to be output.",
)
@click.option(
    "--results-dir",
    "-r",
    required=True,
    metavar="PATH",
    type=Path,
    help="Relative path for results to be output by Phen2gene.",
)
@click.option(
    "--data-dir",
    "-d",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to Phen2Gene data directory.",
)
@click.option(
    "--phenopacket-dir",
    "-p",
    required=False,
    metavar="PATH",
    help="Path to phenopacket directory.",
    cls=MutuallyExclusiveOptionError,
    mutually_exclusive=["input_dir"],
)
@click.option(
    "--input-dir",
    "-i",
    required=False,
    metavar="PATH",
    help="Path to input text file directory.",
    cls=MutuallyExclusiveOptionError,
    mutually_exclusive=["phenopacket_dir"],
)
@click.option(
    "--phen2gene-py",
    "-py",
    required=False,
    metavar="Path",
    type=Path,
    help="Path to Phen2Gene python executable - not required if running with docker.",
)
def prepare_commands_command(
    environment: str,
    file_prefix: str,
    output_dir: Path,
    results_dir: Path,
    data_dir: Path,
    phenopacket_dir: Path or None = None,
    input_dir: Path or None = None,
    phen2gene_py: Path or None = None,
):
    """
    Prepare commands for Phen2Gene.
    Args:
        environment (str): Environment to run Phen2Gene.
        file_prefix (str): Prefix for command file path.
        output_dir (Path): Path to directory to write command file.
        results_dir (Path): Path to the directory to write Phen2Gene results.
        data_dir (Path): Path to the Phen2Gene data directory.
        phenopacket_dir (Path or None): Path to the Phenopacket directory.
        input_dir (Path or None): Path to the input file directory.
        phen2gene_py (Path or None): Path to the Phen2Gene python executable file.
    """
    output_dir.joinpath("tool_input_commands").mkdir(parents=True, exist_ok=True)
    prepare_commands(
        environment,
        file_prefix,
        output_dir.joinpath("tool_input_commands"),
        results_dir,
        data_dir,
        phenopacket_dir,
        input_dir,
        phen2gene_py,
    )
