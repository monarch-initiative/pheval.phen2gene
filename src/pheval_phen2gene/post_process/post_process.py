from pathlib import Path

from pheval_phen2gene.tool_specific_configuration_parser import Phen2GeneToolSpecificConfigurations
from pheval_phen2gene.post_process.post_process_results_format import create_standardised_results


def post_process_results_format(raw_results_dir: Path, output_dir: Path, config: Phen2GeneToolSpecificConfigurations):
    """Create pheval gene result from Phen2Gene tsv output."""
    print("...creating pheval gene results format...")
    create_standardised_results(
        results_dir=raw_results_dir,
        output_dir=output_dir,
        sort_order=config.post_process.score_order,
    )
    print("done")
