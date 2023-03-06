import os
from pathlib import Path

from pheval_phen2gene.config_parser import Phen2GeneConfig
from pheval_phen2gene.post_process.post_process_results_format import create_standardised_results


def post_process_results_format(testdata_dir: Path, output_dir: Path, config: Phen2GeneConfig):
    """Create pheval gene result from Phen2Gene tsv output."""
    print("...creating pheval gene results format...")
    run_output_dir = Path(output_dir).joinpath(
        f"phen2gene" f"{os.sep}{os.path.basename(testdata_dir)}_results"
    )
    create_standardised_results(
        results_dir=Path(run_output_dir).joinpath("phen2gene_results"),
        output_dir=run_output_dir,
        sort_order=config.post_process.score_order,
    )
    print("done")
