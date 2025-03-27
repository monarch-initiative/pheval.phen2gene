from pathlib import Path

import polars as pl
from pheval.post_processing.post_processing import SortOrder, generate_gene_result
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_gene_identifier_map


def read_phen2gene_result(phen2gene_result: Path) -> pl.DataFrame:
    """
    Read Phen2Gene tsv output.
    Args:
        phen2gene_result (Path): Path to the Phen2Gene raw result
    Returns:
        pd.DataFrame: Dataframe containing the Phen2Gene result.
    """
    return pl.read_csv(phen2gene_result, separator="\t")


def extract_gene_results(
    phen2gene_result: pl.DataFrame, gene_identifier_updator: GeneIdentifierUpdater
) -> pl.DataFrame:
    return phen2gene_result.select(
        [
            pl.col("Gene").alias("gene_symbol"),
            pl.col("Gene")
            .map_elements(gene_identifier_updator.find_identifier, return_dtype=pl.String)
            .alias("gene_identifier"),
            pl.col("Score").alias("score").cast(pl.Float64),
        ]
    )


def create_standardised_results(
    results_dir: Path, output_dir: Path, phenopacket_dir: Path, sort_order: str
) -> None:
    """
    Write standardised gene results from default Phen2Gene TSV output.
    Args:
        results_dir (Path): Path to the raw result directory.
        output_dir (Path): Path to the output directory.
        phenopacket_dir (Path): The path to the phenopacket directory.
        sort_order (str): The sort order.
    """
    gene_identifier_updator = GeneIdentifierUpdater(
        identifier_map=create_gene_identifier_map(), gene_identifier="ensembl_id"
    )
    sort_order = SortOrder.ASCENDING if sort_order == "ascending" else SortOrder.DESCENDING
    for result in all_files(results_dir):
        phen2gene_tsv_result = read_phen2gene_result(result)
        pheval_gene_result = extract_gene_results(phen2gene_tsv_result, gene_identifier_updator)
        generate_gene_result(
            results=pheval_gene_result,
            sort_order=sort_order,
            output_dir=output_dir,
            result_path=result,
            phenopacket_dir=phenopacket_dir,
        )
