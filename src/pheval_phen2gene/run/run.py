import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import docker
from pheval.utils.file_utils import all_files

from pheval_phen2gene.prepare.prepare_commands import prepare_commands
from pheval_phen2gene.tool_specific_configuration_parser import Phen2GeneToolSpecificConfigurations


def prepare_phen2gene_commands(
    config: Phen2GeneToolSpecificConfigurations,
    tool_input_commands_dir: Path,
    testdata_dir: Path,
    data_dir: Path,
    raw_results_dir: Path,
):
    """
    Prepare commands to run Phen2Gene.
    Args:
        config (Phen2GeneToolSpecificConfigurations): Phen2Gene tool configurations
        tool_input_commands_dir (Path): Path to the tool input commands directory.
        testdata_dir (Path): Path to the testdata directory.
        data_dir (Path): Path to the data directory.
        raw_results_dir (Path): Path to the directory to write raw results.
    """
    phenopacket_dir = Path(testdata_dir).joinpath("phenopackets")
    prepare_commands(
        environment=config.environment,
        file_prefix=os.path.basename(testdata_dir),
        output_dir=tool_input_commands_dir,
        results_dir=Path(
            os.path.relpath(Path(raw_results_dir)),
            start=os.getcwd(),
        ),
        phenopacket_dir=phenopacket_dir,
        path_to_phen2gene_dir=data_dir.joinpath(config.phen2gene_python_executable),
        data_dir=data_dir.joinpath("lib"),
    )


def run_phen2gene_local(testdata_dir: Path, tool_input_commands_dir: Path):
    """
    Run Phen2Gene locally.
    Args:
        testdata_dir (Path): Path to the testdata directory.
        tool_input_commands_dir (Path): Path to the directory containing tool input commands file.
    """
    batch_file = [
        file
        for file in all_files(tool_input_commands_dir)
        if file.name.startswith(Path(testdata_dir).name)
    ][0]
    print("running phen2gene")
    subprocess.run(
        ["bash", str(batch_file)],
        shell=False,
    )


def read_docker_batch(batch_file: Path) -> [str]:
    """
    Read docker batch file of Phen2Gene commands.
    Args:
        batch_file (Path): Path to the batch file of Phen2Gene commands.
    Returns:
        List[str]: List of docker commands for Phen2Gene.
    """
    with open(batch_file) as batch:
        commands = batch.readlines()
    batch.close()
    return commands


@dataclass
class DockerMounts:
    """
    Mount points for Docker containers.
    Args:
        results_dir (str): Path to the results directory.
        input_dir (str): Path to the input directory.
    """

    results_dir: str
    input_dir: str


def mount_docker(output_dir: Path, input_dir: Path) -> DockerMounts:
    """
    Create Docker mounts for volumes.
    Args:
        output_dir (Path): Path to the output directory.
        input_dir (Path): Path to the input directory.
    Returns:
        DockerMounts: Mount points for docker containers.
    """
    results_dir = f"{output_dir}{os.sep}:/phen2gene-results"
    input_dir = f"{input_dir}{os.sep}:/phen2gene-data"
    return DockerMounts(results_dir=results_dir, input_dir=input_dir)


def run_phen2gene_docker(
    input_dir: Path, testdata_dir: Path, tool_input_commands_dir: Path, raw_results_dir: Path
):
    """
    Run Phen2Gene with docker.
    Args:
        input_dir (Path): Path to the input directory.
        testdata_dir (Path): Path to the test data directory.
        tool_input_commands_dir (Path): Path to the tool input commands directory.
        raw_results_dir (Path): Path to the raw results directory.
    """
    client = docker.from_env()
    batch_file = [
        file
        for file in all_files(tool_input_commands_dir)
        if file.name.startswith(os.path.basename(testdata_dir))
    ][0]
    batch_commands = read_docker_batch(batch_file)
    mounts = mount_docker(
        output_dir=raw_results_dir,
        input_dir=input_dir,
    )
    vol = [mounts.results_dir, mounts.input_dir]
    for command in batch_commands:
        container = client.containers.run(
            "genomicslab/phen2gene",
            command,
            volumes=[str(x) for x in vol],
            detach=True,
        )
        for line in container.logs(stream=True):
            print(line.strip())
        break


def run_phen2gene(
    config: Phen2GeneToolSpecificConfigurations,
    input_dir: Path,
    testdata_dir: Path,
    tool_input_commands_dir: Path,
    raw_results_dir: Path,
):
    """
    Run Phen2Gene.
    Args:
        config (Phen2GeneToolSpecificConfigurations): Phen2Gene tool configurations.
        input_dir (Path): Path to the input directory.
        testdata_dir (Path): Path to the test data directory.
        tool_input_commands_dir (Path): Path to the tool input commands directory.
        raw_results_dir (Path): Path to the raw results directory.
    """
    if config.environment == "docker":
        run_phen2gene_docker(
            input_dir=input_dir,
            testdata_dir=testdata_dir,
            tool_input_commands_dir=tool_input_commands_dir,
            raw_results_dir=raw_results_dir,
        )
    if config.environment == "local":
        run_phen2gene_local(
            testdata_dir=testdata_dir, tool_input_commands_dir=tool_input_commands_dir
        )
