from pathlib import Path
from typing import List

import click
import pandas as pd
from pheval.post_processing.post_processing import PhEvalGeneResult, generate_pheval_result
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_phen2gene_result(phen2gene_result: Path) -> pd.DataFrame:
    """
    Read Phen2Gene tsv output.
    Args:
        phen2gene_result (Path): Path to the phen2gene raw result
    Returns:
        pd.DataFrame: Dataframe containing the phen2gene result.
    """
    return pd.read_csv(phen2gene_result, delimiter="\t")


class PhEvalGeneResultFromPhen2GeneTsvCreator:
    """Class for converting Phen2Gene raw result to PhEval gene result.t"""

    def __init__(
        self, phen2gene_tsv_result: pd.DataFrame, gene_identifier_updator: GeneIdentifierUpdater
    ):
        """
        Initialise the PhEvalGeneResultFromPhen2Gene class.
        Args:
            phen2gene_tsv_result (pd.DataFrame): Phen2Gene result.
            gene_identifier_updator (GeneIdentifierUpdater): GeneIdentifierUpdater object.
        """
        self.phen2gene_tsv_result = phen2gene_tsv_result
        self.gene_identifier_updator = gene_identifier_updator

    @staticmethod
    def _find_gene_symbol(result_entry: pd.Series) -> str:
        """
        Return gene symbol from Phen2Gene result entry.
        Args:
            result_entry (pd.Series): Phen2Gene result entry
        Returns:
            str: The gene symbol
        """
        return result_entry["Gene"]

    def _find_ensembl_identifier(self, result_entry: pd.Series) -> str:
        """
        Return ensembl gene identifier from Phen2Gene result entry.
        Args:
            result_entry (pd.Series): Phen2Gene result entry.
        Returns:
            str: The ensembl gene identifier.
        """
        return self.gene_identifier_updator.find_identifier(result_entry["Gene"])

    @staticmethod
    def _find_relevant_score(result_entry: pd.Series) -> float:
        """
        Return score from Phen2Gene result entry.
        Args:
            result_entry (pd.Series): Phen2Gene result entry.
        Returns:
            float: The score.
        """
        return round(result_entry["Score"], 4)

    def extract_pheval_gene_requirements(self) -> List[PhEvalGeneResult]:
        """
        Extract data required to produce PhEval gene output.
        Returns:
            List[PhEvalGeneResult]: List of PhEvalGeneResult objects.
        """
        simplified_phen2gene_result = []
        for _index, row in self.phen2gene_tsv_result.iterrows():
            simplified_phen2gene_result.append(
                PhEvalGeneResult(
                    gene_symbol=self._find_gene_symbol(row),
                    gene_identifier=self._find_ensembl_identifier(row),
                    score=self._find_relevant_score(row),
                )
            )
        return simplified_phen2gene_result


def create_standardised_results(results_dir: Path, output_dir: Path, sort_order: str) -> None:
    """
    Write standardised gene results from default Phen2Gene TSV output.
    Args:
        results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory.
        sort_order (str): The sort order of the results, either ascending or descending.
    """
    hgnc_data = create_hgnc_dict()
    gene_identifier_updator = GeneIdentifierUpdater(
        hgnc_data=hgnc_data, gene_identifier="ensembl_id"
    )
    for result in all_files(results_dir):
        phen2gene_tsv_result = read_phen2gene_result(result)
        pheval_gene_result = PhEvalGeneResultFromPhen2GeneTsvCreator(
            phen2gene_tsv_result, gene_identifier_updator
        ).extract_pheval_gene_requirements()
        generate_pheval_result(
            pheval_result=pheval_gene_result,
            sort_order_str=sort_order,
            output_dir=output_dir,
            tool_result_path=result,
        )


@click.command()
@click.option(
    "--results-dir",
    "-r",
    metavar="Path",
    required=True,
    help="Path to file to be standardised",
    type=Path,
)
@click.option(
    "--output-dir",
    "-o",
    metavar="Path",
    required=True,
    help="Path to the output directory.",
    type=Path,
)
@click.option(
    "--sort-order",
    "-so",
    required=True,
    help="Ordering of results for ranking.",
    type=click.Choice(["ascending", "descending"]),
    default="descending",
    show_default=True,
)
def post_process_phen2gene_results(results_dir: Path, output_dir: Path, sort_order: str) -> None:
    """
    Post-process Phen2Gene .tsv results to PhEval gene result format.
    Args:
        results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory to write PhEval gene result format.
        sort_order (str): Ordering of results for ranking.
    """
    create_standardised_results(output_dir, results_dir, sort_order)
