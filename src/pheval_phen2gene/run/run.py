import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import docker
from pheval.utils.file_utils import all_files

from pheval_phen2gene.utils.phen2gene_config_parser import Phen2GeneConfig
from pheval_phen2gene.prepare.prepare_commands import prepare_commands


def prepare_phen2gene_commands(
    config: Phen2GeneConfig, output_dir: Path, testdata_dir: Path, data_dir: Path
):
    """Prepare commands to run Phen2Gene."""
    Path(output_dir).joinpath("phen2gene").mkdir(parents=True, exist_ok=True)
    phenopacket_dir = Path(testdata_dir).joinpath(
        [
            directory
            for directory in os.listdir(str(testdata_dir))
            if "phenopacket" in str(directory)
        ][0]
    )
    prepare_commands(
        environment=config.run.environment,
        file_prefix=os.path.basename(testdata_dir),
        output_dir=Path(output_dir).joinpath("phen2gene"),
        results_dir=Path(
            os.path.relpath(
                Path(output_dir).joinpath(
                    f"phen2gene/{os.path.basename(testdata_dir)}_results/phen2gene_results/",
                )
            ),
            start=os.getcwd(),
        ),
        phenopacket_dir=phenopacket_dir,
        path_to_phen2gene_dir=config.run.path_to_phen2gene_executable,
        data_dir=data_dir,
    )


def run_phen2gene_local(testdata_dir: Path, output_dir: Path):
    """Run Phen2Gene locally."""
    Path(output_dir).joinpath(
        f"phen2gene/{os.path.basename(testdata_dir)}_results/phen2gene_results"
    ).mkdir(parents=True, exist_ok=True)
    batch_file = [
        file
        for file in all_files(Path(output_dir).joinpath("phen2gene/phen2gene_batch_files"))
        if file.name.startswith(os.path.basename(testdata_dir))
    ][0]
    subprocess.run(
        ["activate", "phen2gene"],
        shell=False,
    )
    print("activated phen2gene conda environment")
    print("running phen2gene")
    subprocess.run(
        ["bash", str(batch_file)],
        shell=False,
    )


def read_docker_batch(batch_file: Path) -> [str]:
    """Read docker batch file of Phen2Gene commands."""
    with open(batch_file) as batch:
        commands = batch.readlines()
    batch.close()
    return commands


@dataclass
class DockerMounts:
    results_dir: str
    input_dir: str


def mount_docker(output_dir: Path, input_dir: Path) -> DockerMounts:
    """Create Docker mounts for volumes."""
    results_dir = f"{output_dir}{os.sep}:/phen2gene-results"
    input_dir = f"{input_dir}{os.sep}:/phen2gene-data"
    return DockerMounts(results_dir=results_dir, input_dir=input_dir)


def run_phen2gene_docker(input_dir: Path, testdata_dir: Path, output_dir: Path):
    """Run Phen2Gene with docker"""
    client = docker.from_env()
    results_sub_output_dir = Path(output_dir).joinpath(f"phen2gene{os.sep}")
    batch_file = [
        file
        for file in all_files(Path(results_sub_output_dir).joinpath("phen2gene_batch_files"))
        if file.name.startswith(os.path.basename(testdata_dir))
    ][0]
    batch_commands = read_docker_batch(batch_file)
    mounts = mount_docker(
        output_dir=results_sub_output_dir.joinpath(
            f"{os.path.basename(testdata_dir)}_results/pheval_gene_results"
        ),
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


def run_phen2gene(config: Phen2GeneConfig, input_dir: Path, testdata_dir: Path, output_dir: Path):
    """Run Phen2Gene."""
    if config.run.environment == "docker":
        run_phen2gene_docker(input_dir=input_dir, testdata_dir=testdata_dir, output_dir=output_dir)
    if config.run.environment == "local":
        run_phen2gene_local(testdata_dir=testdata_dir, output_dir=output_dir)
