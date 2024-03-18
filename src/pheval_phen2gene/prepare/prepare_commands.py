import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class Phen2GeneCommandLineArguments:
    """
    Minimal arguments required to run Phen2Gene on the command line.
    Args:
        path_to_phen2gene_dir (Path): Path to the Phen2Gene directory
        output_dir (Path): Path to the output directory.
        output_file_name (Path): Name of the output file.
        input_file_path (Path): Path to the input file.
        hpo_ids (List[str]): List of hpo ids.
    """

    path_to_phen2gene_dir: Path
    output_dir: Path
    output_file_name: Path
    input_file_path: [Path] = None
    hpo_ids: List[str] = None


@dataclass
class Phen2GeneDockerArguments:
    """
    Minimal arguments required to run Phen2Gene on docker.
    Args:
        output_dir (Path): Path to the output directory.
        output_file_name (Path): Name of the output file.
        input_file_path (Path): Path to the input file
        hpo_ids (List[str]): List of hpo ids.
    """

    output_dir: Path
    output_file_name: Path
    input_file_path: [Path] = None
    hpo_ids: List[str] = None


def create_command_line_arguments(
    path_to_phen2gene_dir: Path,
    output_dir: Path,
    output_file_name: Path,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> Phen2GeneCommandLineArguments:
    """
    Create command line arguments required for Phen2Gene.
    Args:
        path_to_phen2gene_dir (Path): Path to the Phen2Gene directory.
        output_dir (Path): Path to the output directory.
        output_file_name (Path): Name of the output file.
        input_file_path (Path or None): Path to the input file.
        phenopacket_path (Path or None): Path to the phenopacket.
    Returns:
        Phen2GeneCommandLineArguments: Arguments required to run Phen2Gene.
    """
    if phenopacket_path is None:
        return Phen2GeneCommandLineArguments(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=output_file_name,
            input_file_path=input_file_path,
        )
    if input_file_path is None:
        phenopacket = phenopacket_reader(phenopacket_path)
        return Phen2GeneCommandLineArguments(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=output_file_name,
            hpo_ids=[
                hpo.type.id for hpo in PhenopacketUtil(phenopacket).observed_phenotypic_features()
            ],
        )


def create_docker_arguments(
    output_dir: Path,
    output_file_name: Path,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> Phen2GeneDockerArguments:
    """
    Create the docker arguments required for Phen2Gene.
    Args:
        output_dir (Path): Path to the output directory.
        output_file_name (Path): Name of the output file.
        input_file_path (Path or None): Path to the input file.
        phenopacket_path (Path or None): Path to the phenopacket.
    """
    if phenopacket_path is None:
        return Phen2GeneDockerArguments(
            output_dir=output_dir,
            output_file_name=output_file_name,
            input_file_path=input_file_path,
        )
    if input_file_path is None:
        phenopacket = phenopacket_reader(phenopacket_path)
        return Phen2GeneDockerArguments(
            output_dir=output_dir,
            output_file_name=output_file_name,
            hpo_ids=[
                hpo.type.id for hpo in PhenopacketUtil(phenopacket).observed_phenotypic_features()
            ],
        )


class CommandWriter:
    """Class for writing all commands to a text file."""

    def __init__(self, output_file: Path):
        """
        Initialise the CommandWriter class.
        Args:
            output_file (Path): Path to the output file to write commands.
        """
        self.file = open(output_file, "w")

    def write_local_command(
        self, command_arguments: Phen2GeneCommandLineArguments, data_dir: Path
    ) -> None:
        """
        Write a Phen2Gene command to run locally.
        Args:
            command_arguments (Phen2GeneCommandLineArguments): Phen2Gene command line arguments.
            data_dir (Path): Path to Phen2Gene input data directory.
        """
        try:
            if command_arguments.hpo_ids is None:
                # TODO create this as a list instead in another method and then do "\n".join here
                # TODO so that I can test that it was done correctly
                self.file.write(
                    "python3 "
                    + str(command_arguments.path_to_phen2gene_dir)
                    + " --file "
                    + str(command_arguments.input_file_path)
                    + " -out "
                    + f"{str(command_arguments.output_dir)}{os.sep}"
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + " -d "
                    + str(data_dir)
                    + "\n"
                )
            if command_arguments.input_file_path is None:
                self.file.write(
                    "python3 "
                    + str(command_arguments.path_to_phen2gene_dir)
                    + " --manual "
                    + " ".join(command_arguments.hpo_ids)
                    + " -out "
                    + f"{str(command_arguments.output_dir)}{os.sep}"
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + " -d "
                    + str(data_dir)
                    + "\n"
                )
        except IOError:
            print("Error writing ", self.file)

    def write_docker_command(self, command_arguments: Phen2GeneDockerArguments) -> None:
        """
        Write a Phen2Gene command to run with docker.
        Args:
            command_arguments (Phen2GeneDockerArguments): Arguments passed to docker command for Phen2Gene.
        """
        try:
            if command_arguments.hpo_ids is None:
                self.file.write(
                    " --file "
                    + str(command_arguments.input_file_path)
                    + " -out "
                    + "/phen2gene-results"
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + " -d "
                    + "/phen2gene-data"
                    + "\n"
                )
            if command_arguments.input_file_path is None:
                self.file.write(
                    " --manual "
                    + " ".join(command_arguments.hpo_ids)
                    + " -out "
                    + "/phen2gene-results"
                    + " --name "
                    + str(command_arguments.output_file_name)
                    + " -d "
                    + "/phen2gene-data"
                    + "\n"
                )
        except IOError:
            print("Error writing ", self.file)

    def close(self):
        """Close the file."""
        self.file.close()


def write_single_local_command(
    path_to_phen2gene_dir: Path,
    output_dir: Path,
    output_file_name: Path,
    data_dir: Path,
    command_writer: CommandWriter,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> None:
    """
    Write a single command locally when given either a phenopacket or prepared input file.
    Args:
        path_to_phen2gene_dir (Path): Path to the Phen2Gene directory.
        output_dir (Path): Path to the output directory.
        output_file_name (Path): Name of the output file.
        data_dir (Path): Path to the Phen2Gene data directory.
        command_writer (CommandWriter): CommandWriter instance.
        input_file_path (Path or None): Path to the input file.
        phenopacket_path (Path or None): Path to the phenopacket.
    """
    arguments = create_command_line_arguments(
        path_to_phen2gene_dir=path_to_phen2gene_dir,
        output_dir=output_dir,
        output_file_name=output_file_name,
        input_file_path=input_file_path,
        phenopacket_path=phenopacket_path,
    )
    command_writer.write_local_command(arguments, data_dir)


def write_single_docker_command(
    output_dir: Path,
    output_file_name: Path,
    command_writer: CommandWriter,
    input_file_path: Path or None = None,
    phenopacket_path: Path or None = None,
) -> None:
    """
    Write a docker command when given either a phenopacket or prepared input file.
    Args:
        output_dir (Path): Path to the output directory.
        output_file_name (Path): Name of the output file.
        command_writer (CommandWriter): CommandWriter instance.
        input_file_path (Path or None): Path to the input file.
        phenopacket_path (Path or None): Path to the phenopacket.
    """
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
    data_dir: Path,
    phenopacket_dir: Path or None,
    input_dir: Path or None,
) -> None:
    """
    Write all commands to run locally when given either directory containing phenopackets or input files.
    Args:
        path_to_phen2gene_dir (Path): Path to the Phen2Gene directory.
        command_file_path (Path): Path to the file to write commands.
        output_dir (Path): Path to the output directory.
        data_dir (Path): Path to the Phen2Gene data directory.
        phenopacket_dir (Path or None): Path to the phenopacket directory.
        input_dir (Path or None): Path to the input file directory.
    """
    input_files = all_files(phenopacket_dir) if input_dir is None else all_files(input_dir)
    command_writer = CommandWriter(command_file_path)
    for input_file in input_files:
        (
            write_single_local_command(
                path_to_phen2gene_dir=path_to_phen2gene_dir,
                output_dir=output_dir,
                output_file_name=Path(input_file.stem),
                command_writer=command_writer,
                input_file_path=input_file,
                data_dir=data_dir,
            )
            if phenopacket_dir is None
            else write_single_local_command(
                path_to_phen2gene_dir=path_to_phen2gene_dir,
                output_dir=output_dir,
                output_file_name=Path(input_file.stem),
                command_writer=command_writer,
                phenopacket_path=input_file,
                data_dir=data_dir,
            )
        )
    command_writer.close()


def write_docker_commands(
    command_file_path: Path,
    output_dir: Path,
    phenopacket_dir: Path or None,
    input_dir: Path or None,
) -> None:
    """
    Write all commands to run with docker when given either directory containing phenopackets or input files.
    Args:
        command_file_path (Path): Path to the file to write commands.
        output_dir (Path): Path to the output directory.
        phenopacket_dir (Path or None): Path to the phenopacket directory.
        input_dir (Path or None): Path to the input file directory.
    """
    input_files = all_files(phenopacket_dir) if input_dir is None else all_files(input_dir)
    command_writer = CommandWriter(command_file_path)
    for input_file in input_files:
        (
            write_single_docker_command(
                output_dir=output_dir,
                output_file_name=Path(input_file.stem),
                command_writer=command_writer,
                phenopacket_path=input_file,
            )
            if input_dir is None
            else write_single_docker_command(
                output_dir=output_dir,
                output_file_name=Path(input_file.stem),
                command_writer=command_writer,
                input_file_path=input_file,
            )
        )


def prepare_commands(
    environment: str,
    file_prefix: str,
    output_dir: Path,
    results_dir: Path,
    data_dir: Path,
    phenopacket_dir: Path or None = None,
    input_dir: Path or None = None,
    path_to_phen2gene_dir: Path or None = None,
) -> None:
    """
    Prepare all commands to run with Phen2Gene.
    Args:
        environment (str): Environment to run Phen2Gene commands.
        file_prefix (str): Prefix for command file path.
        output_dir (Path): Path to the directory to write command file.
        results_dir (Path): Path to the directory to write Phen2Gene results.
        data_dir (Path): Path to the Phen2Gene data directory.
        phenopacket_dir (Path or None): Path to the phenopacket directory.
        input_dir (Path or None): Path to the input file directory.
        path_to_phen2gene_dir (Path or None): Path to the Phen2Gene directory.
    """
    command_file_path = output_dir.joinpath(f"{file_prefix}-phen2gene-batch.txt")
    if environment == "local":
        write_local_commands(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            command_file_path=command_file_path,
            phenopacket_dir=phenopacket_dir,
            input_dir=input_dir,
            output_dir=results_dir,
            data_dir=data_dir,
        )
    if environment == "docker":
        write_docker_commands(
            command_file_path=command_file_path,
            output_dir=results_dir,
            phenopacket_dir=phenopacket_dir,
            input_dir=input_dir,
        )
