from pathlib import Path

from pheval_phen2gene.post_process.post_process_results_format import create_standardised_results
from pheval_phen2gene.tool_specific_configuration_parser import Phen2GeneToolSpecificConfigurations


def post_process_results_format(
    raw_results_dir: Path,
    output_dir: Path,
    phenopacket_dir: Path,
    config: Phen2GeneToolSpecificConfigurations,
):
    """
    Create pheval gene result from Phen2Gene tsv output.
    Args:
        raw_results_dir (Path): Path to the raw result directory.
        output_dir (Path): Path to the output directory.
        phenopacket_dir (Path): Path to the phenopacket directory.
        config (Phen2GeneToolSpecificConfigurations): Phen2Gene tool configurations.
    """
    print("...creating pheval gene results format...")
    create_standardised_results(
        results_dir=raw_results_dir,
        output_dir=output_dir,
        phenopacket_dir=phenopacket_dir,
        sort_order=config.post_process.score_order,
    )
    print("done")
