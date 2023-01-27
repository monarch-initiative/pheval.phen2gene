import os
import subprocess
from pathlib import Path

from pheval.utils.file_utils import all_files

from pheval_phen2gene.phen2gene_config_parser import Phen2GeneConfig
from pheval_phen2gene.prepare.prepare_commands import prepare_commands


def prepare_phen2gene_commands(config: Phen2GeneConfig, output_dir: Path, testdata_dir: Path):
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
        results_dir=Path(output_dir).joinpath(
            f"phen2gene/{os.path.basename(testdata_dir)}_results/phen2gene_results/"
        ),
        phenopacket_dir=phenopacket_dir,
        path_to_phen2gene_dir=config.run.path_to_phen2gene_software_directory,
    )


def run_phen2gene_local(testdata_dir: Path, output_dir: Path):
    try:
        Path(output_dir).joinpath(
            f"phen2gene/{os.path.basename(testdata_dir)}_results/phen2gene_results"
        ).mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass
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
