from pathlib import Path

import click
from pheval.prepare.custom_exceptions import MutuallyExclusiveOptionError

from pheval_phen2gene.prepare.prepare_commands import prepare_commands
from pheval_phen2gene.prepare.prepare_inputs import prepare_input, prepare_inputs


@click.command("prepare-input")
@click.option(
    "--phenopacket-path",
    "-p",
    required=True,
    metavar="FILE",
    help="Path to phenopacket.",
    type=Path,
)
@click.option(
    "--output-dir", "-o", required=True, metavar="PATH", help="Path to output directory.", type=Path
)
def prepare_input_command(phenopacket_path: Path, output_dir: Path):
    """Create the input file required for running Phen2Gene from a phenopacket."""
    prepare_input(phenopacket_path=phenopacket_path, output_dir=output_dir)


@click.command("prepare-inputs")
@click.option(
    "--phenopacket-dir", "-p", required=True, metavar="FILE", help="Path to phenopacket.", type=Path
)
@click.option(
    "--output-dir", "-o", required=True, metavar="PATH", help="Path to output directory.", type=Path
)
def prepare_inputs_command(phenopacket_dir: Path, output_dir: Path):
    """Create input files required for running Phen2Gene from phenopackets."""
    prepare_inputs(phenopacket_dir=phenopacket_dir, output_dir=output_dir)


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
    "--phenopacket-dir",
    "-P",
    cls=MutuallyExclusiveOptionError,
    mutually_exclusive=["input_dir"],
    required=False,
    metavar="PATH",
    type=Path,
    help="Path to the phenopacket directory. ",
)
@click.option(
    "--phen2gene-py",
    "-s",
    required=False,
    metavar="PATH",
    type=Path,
    help="Full path to Phen2Gene python executable.",
)
@click.option(
    "--input-dir",
    "-i",
    cls=MutuallyExclusiveOptionError,
    mutually_exclusive=["phenopacket_dir"],
    required=False,
    metavar="PATH",
    type=Path,
    help="Path to the prepared input files for Phen2Gene. ",
)
@click.option(
    "--file-prefix",
    "-p",
    required=False,
    metavar="TEXT",
    help="Prefix of generated command file.",
    default="RUN",
    show_default=True,
    type=str,
)
@click.option(
    "--results-dir",
    "-r",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to the results directory.",
)
@click.option(
    "--data-dir",
    "-d",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to the Phen2Gene data directory.",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to the output directory for batch files.",
)
def prepare_commands_command(
    environment: str,
    file_prefix: str,
    output_dir: Path,
    results_dir: Path,
    data_dir: Path,
    phen2gene_py: Path or None = None,
    phenopacket_dir: Path = None,
    input_dir: Path = None,
) -> None:
    """Prepare a text file containing all commands to run Phen2Gene from either phenopackets
    or a prepared set of inputs."""
    prepare_commands(
        environment=environment,
        file_prefix=file_prefix,
        output_dir=output_dir,
        phenopacket_dir=phenopacket_dir,
        input_dir=input_dir,
        path_to_phen2gene_dir=phen2gene_py,
        results_dir=results_dir,
        data_dir=data_dir,
    )
