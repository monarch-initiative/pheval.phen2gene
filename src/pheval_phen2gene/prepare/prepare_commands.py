from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import click
from pheval.prepare.custom_exceptions import MutuallyExclusiveOptionError
from pheval.utils.file_utils import all_files

from src.pheval_phen2gene.prepare.prepare_inputs import extract_proband_hpo_ids


@dataclass
class Phen2GeneCommandLineArguments:
    """Minimal arguments required to run Phen2Gene on the command line."""

    path_to_phen2gene_dir: Path
    output_dir: Path
    output_file_name: Path
    input_file_path: Optional[Path] = None
    hpo_ids: List[str] = None


@dataclass
class Phen2GeneDockerArguments:
    """Minimal arguments required to run Phen2Gene on docker."""

    output_dir: Path
    output_file_name: Path
    input_file_path: Optional[Path] = None
    hpo_ids: List[str] = None


def create_command_line_arguments(
    path_to_phen2gene_dir: Path,
    output_dir: Path,
    output_file_name: Path,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> Phen2GeneCommandLineArguments:
    """Create the command line arguments required for Phen2Gene."""
    if phenopacket_path is None:
        return Phen2GeneCommandLineArguments(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=output_file_name,
            input_file_path=input_file_path,
        )
    if input_file_path is None:
        return Phen2GeneCommandLineArguments(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=output_file_name,
            hpo_ids=extract_proband_hpo_ids(phenopacket_path),
        )


def create_docker_arguments(
    output_dir: Path,
    output_file_name: Path,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> Phen2GeneDockerArguments:
    """Create the docker arguments required for Phen2Gene."""
    if phenopacket_path is None:
        return Phen2GeneDockerArguments(
            output_dir=output_dir,
            output_file_name=output_file_name,
            input_file_path=input_file_path,
        )
    if input_file_path is None:
        return Phen2GeneDockerArguments(
            output_dir=output_dir,
            output_file_name=output_file_name,
            hpo_ids=extract_proband_hpo_ids(phenopacket_path),
        )


class CommandWriter:
    """Write all commands to a text file."""

    def __init__(self, output_file: Path):
        self.file = open(output_file, "a")

    def write_local_command(self, command_arguments: Phen2GeneCommandLineArguments) -> None:
        """Write a Phen2Gene command to run locally."""
        try:
            if command_arguments.hpo_ids is None:
                self.file.write(
                    "python3 "
                    + str(command_arguments.path_to_phen2gene_dir)
                    + " --file "
                    + str(command_arguments.input_file_path)
                    + " -out "
                    + str(command_arguments.output_dir)
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + "\n"
                )
            if command_arguments.input_file_path is None:
                self.file.write(
                    "python3 "
                    + str(command_arguments.path_to_phen2gene_dir)
                    + " --manual "
                    + " ".join(command_arguments.hpo_ids)
                    + " -out "
                    + str(command_arguments.output_dir)
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + "\n"
                )
        except IOError:
            print("Error writing ", self.file)

    def write_docker_command(self, command_arguments: Phen2GeneDockerArguments) -> None:
        """Write a Phen2Gene command to run with docker."""
        try:
            if command_arguments.hpo_ids is None:
                self.file.write(
                    " --file "
                    + str(command_arguments.input_file_path)
                    + " -out "
                    + str(command_arguments.output_dir)
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + "\n"
                )
            if command_arguments.input_file_path is None:
                self.file.write(
                    " --manual "
                    + " ".join(command_arguments.hpo_ids)
                    + " -out "
                    + str(command_arguments.output_dir)
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + "\n"
                )
        except IOError:
            print("Error writing ", self.file)

    def close(self):
        self.file.close()


def write_single_local_command(
    path_to_phen2gene_dir: Path,
    output_dir: Path,
    output_file_name: Path,
    command_writer: CommandWriter,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> None:
    """Write a single command locally when given either a phenopacket or prepared input file."""
    arguments = create_command_line_arguments(
        path_to_phen2gene_dir=path_to_phen2gene_dir,
        output_dir=output_dir,
        output_file_name=output_file_name,
        input_file_path=input_file_path,
        phenopacket_path=phenopacket_path,
    )
    command_writer.write_local_command(arguments)


def write_single_docker_command(
    output_dir: Path,
    output_file_name: Path,
    command_writer: CommandWriter,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> None:
    """Write a docker command when given either a phenopacket or prepared input file."""
    arguments = create_docker_arguments(
        output_dir=output_dir,
        output_file_name=output_file_name,
        input_file_path=input_file_path,
        phenopacket_path=phenopacket_path,
    )
    command_writer.write_docker_command(arguments)


def write_local_commands(
    path_to_phen2gene_dir: Path,
    command_file_path: Path,
    output_dir: Path,
    phenopacket_dir: Path or None,
    input_dir: Path or None,
) -> None:
    """Write all commands to run locally when given either phenopacket or input directory."""
    input_files = all_files(phenopacket_dir) if input_dir is None else all_files(input_dir)
    command_writer = CommandWriter(command_file_path)
    for input_file in input_files:
        write_single_local_command(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=Path(input_file.stem),
            command_writer=command_writer,
            input_file_path=input_file,
        ) if phenopacket_dir is None else write_single_local_command(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=Path(input_file.stem),
            command_writer=command_writer,
            phenopacket_path=input_file,
        )
    command_writer.close()


def write_docker_commands(
    command_file_path: Path,
    output_dir: Path,
    phenopacket_dir: Path or None,
    input_dir: Path or None,
) -> None:
    input_files = all_files(phenopacket_dir) if input_dir is None else all_files(input_dir)
    command_writer = CommandWriter(command_file_path)
    """Write all commands to run with docker when given either phenopacket or input directory."""
    for input_file in input_files:
        write_single_docker_command(
            output_dir=output_dir,
            output_file_name=Path(input_file.stem),
            command_writer=command_writer,
            phenopacket_path=input_file,
        ) if input_dir is None else write_single_docker_command(
            output_dir=output_dir,
            output_file_name=Path(input_file.stem),
            command_writer=command_writer,
            input_file_path=input_file,
        )


def prepare_commands(
    environment: str,
    file_prefix: str,
    output_dir: Path,
    phenopacket_dir: Path or None = None,
    input_dir: Path or None = None,
    path_to_phen2gene_dir: Path or None = None,
) -> None:
    """Prepare all commands to run with Phen2Gene."""
    try:
        output_dir.mkdir()
        # command_file_path.parents[0].mkdir()
    except FileExistsError:
        pass
    try:
        output_dir.joinpath("phen2gene_batch_files").mkdir()
    except FileExistsError:
        pass
    command_file_path = output_dir.joinpath(
        f"phen2gene_batch_files/{file_prefix}-phen2gene_batch.txt"
    )
    if environment == "local":
        write_local_commands(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            command_file_path=command_file_path,
            phenopacket_dir=phenopacket_dir,
            input_dir=input_dir,
            output_dir=output_dir,
        )
    if environment == "docker":
        write_docker_commands(
            command_file_path=command_file_path,
            output_dir=output_dir,
            phenopacket_dir=phenopacket_dir,
            input_dir=input_dir,
        )


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
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to the output directory.",
)
def prepare_commands_command(
    environment: str,
    file_prefix: str,
    output_dir: Path,
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
    )
