import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class Phen2GeneCommandLineArguments:
    """Minimal arguments required to run Phen2Gene on the command line."""

    path_to_phen2gene_dir: Path
    output_dir: Path
    output_file_name: Path
    input_file_path: [Path] = None
    hpo_ids: List[str] = None


@dataclass
class Phen2GeneDockerArguments:
    """Minimal arguments required to run Phen2Gene on docker."""

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
    """Create command line arguments required for Phen2Gene."""
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
    """Create the docker arguments required for Phen2Gene."""
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
    """Write all commands to a text file."""

    def __init__(self, output_file: Path):
        self.file = open(output_file, "w")

    def write_local_command(
            self, command_arguments: Phen2GeneCommandLineArguments, data_dir
    ) -> None:
        """Write a Phen2Gene command to run locally."""
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
        """Write a Phen2Gene command to run with docker."""
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
    """Write a single command locally when given either a phenopacket or prepared input file."""
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
        data_dir: Path,
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
            data_dir=data_dir,
        ) if phenopacket_dir is None else write_single_local_command(
            path_to_phen2gene_dir=path_to_phen2gene_dir,
            output_dir=output_dir,
            output_file_name=Path(input_file.stem),
            command_writer=command_writer,
            phenopacket_path=input_file,
            data_dir=data_dir,
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
        results_dir: Path,
        data_dir: Path,
        phenopacket_dir: Path or None = None,
        input_dir: Path or None = None,
        path_to_phen2gene_dir: Path or None = None,
) -> None:
    """Prepare all commands to run with Phen2Gene."""
    output_dir.joinpath("phen2gene_batch_files").mkdir(parents=True, exist_ok=True)
    command_file_path = output_dir.joinpath(
        f"phen2gene_batch_files/{file_prefix}-phen2gene-batch.txt"
    )
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
