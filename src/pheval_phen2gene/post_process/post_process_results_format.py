from pathlib import Path

import click
import pandas as pd
from pheval.post_processing.post_processing import PhEvalGeneResult
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_phen2gene_result(phen2gene_result: Path):
    """Read Phen2Gene tsv output."""
    return pd.read_csv(phen2gene_result, delimiter="\t")


class PhEvalGeneResultFromPhen2GeneTsvCreator:
    def __init__(self, phen2gene_tsv_result:pd.DataFrame, gene_identifier_updator: GeneIdentifierUpdater):
        self.phen2gene_tsv_result = phen2gene_tsv_result
        self.gene_identifier_updator = gene_identifier_updator

    @staticmethod
    def find_gene_symbol(result_entry: pd.Series) -> str:
        return result_entry["Gene"]

    def find_ensembl_identifier(self, result_entry: pd.Series) -> str:
        return self.gene_identifier_updator.find_identifier(result_entry["Gene"])

    @staticmethod
    def find_relevant_score(result_entry: pd.Series) -> float:
        return round(result_entry["Score"], 4)

    def extract_pheval_gene_requirements(self) -> [PhEvalGeneResult]:
        simplified_phen2gene_result = []
        for _index, row in self.phen2gene_tsv_result.iterrows():
            simplified_phen2gene_result.append(PhEvalGeneResult(gene_symbol=self.find_gene_symbol(row),
                                                                gene_identifier=self.find_ensembl_identifier(row),
                                                                score=self.find_relevant_score(row)))
        return simplified_phen2gene_result




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
def post_process_phen2gene_results(results_dir: Path, output_dir: Path) -> None:
    """Post-process Phen2Gene .tsv results to PhEval gene result format."""
    pass
    # create_standardised_results(output_dir, results_dir)
