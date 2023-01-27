from pathlib import Path

import click
import pandas as pd
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_phen2gene_result(phen2gene_result: Path):
    return pd.read_csv(phen2gene_result, delimiter="\t")


class StandardisePhen2GeneResult:
    def __init__(self, gene_result: pd.DataFrame, gene_identifier_updater: GeneIdentifierUpdater):
        self.gene_result = gene_result
        self.gene_identifier_updater = gene_identifier_updater

    def add_ensembl_identifier(self, gene_symbol: str):
        return self.gene_identifier_updater.find_identifier(gene_symbol)

    def create_result_dictionary(self, result_entry: pd.Series):
        return {
            "gene_symbol": result_entry["Gene"],
            "gene_identifier": self.add_ensembl_identifier(result_entry["Gene"]),
            "score": round(result_entry["Score"], 4),
        }

    def simplify_result(self, standardised_result: []):
        for _index, row in self.gene_result.iterrows():
            standardised_result.append(self.create_result_dictionary(row))
        return standardised_result

    @staticmethod
    def sort_result(standardised_result: []):
        return sorted(
            standardised_result,
            key=lambda d: d["score"],
            reverse=True,
        )

    @staticmethod
    def add_ranks(standardised_result: []):
        rank, count, previous = 0, 0, None
        for result in standardised_result:
            count += 1
            if result["score"] != previous:
                rank += count
                previous = result["score"]
                count = 0
            result["rank"] = rank
        return standardised_result

    def standardise_gene_result(self):
        result = []
        simplified_result = self.simplify_result(result)
        sorted_result = self.sort_result(simplified_result)
        return self.add_ranks(sorted_result)


def create_standardised_results(output_dir: Path, results_dir: Path) -> None:
    output_dir.joinpath("pheval_gene_results/").mkdir(exist_ok=True)
    hgnc_dict = create_hgnc_dict()
    gene_identifier_updater = GeneIdentifierUpdater(hgnc_dict, "ensembl_id")
    for result in all_files(results_dir):
        gene_result = read_phen2gene_result(result)
        standardised_gene_result = StandardisePhen2GeneResult(
            gene_result, gene_identifier_updater
        ).standardise_gene_result()
        gene_df = pd.DataFrame(standardised_gene_result)
        gene_df = gene_df.loc[:, ["rank", "score", "gene_symbol", "gene_identifier"]]
        gene_df.to_csv(
            output_dir.joinpath(
                "pheval_gene_results/" + result.stem + "-phen2gene-pheval_gene_result.tsv"
            ),
            sep="\t",
            index=False,
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
def post_process_phen2gene_results(results_dir: Path, output_dir: Path) -> None:
    create_standardised_results(output_dir, results_dir)
