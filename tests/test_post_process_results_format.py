import unittest

import polars as pl
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_gene_identifier_map

from pheval_phen2gene.post_process.post_process_results_format import extract_gene_results

example_phen2gene_result = pl.DataFrame(
    [
        {"Rank": 1, "Gene": "GCDH", "ID": "2639", "Score": 1.0, "Status": "SeedGene"},
        {"Rank": 2, "Gene": "ETFB", "ID": "2109", "Score": 0.298386, "Status": "SeedGene"},
        {"Rank": 3, "Gene": "ETFA", "ID": "2108", "Score": 0.286989, "Status": "SeedGene"},
    ]
)


class TestExtractGeneResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gene_identifier_updator = GeneIdentifierUpdater(
            identifier_map=create_gene_identifier_map(), gene_identifier="ensembl_id"
        )

    def test_extract_gene_results(self):
        self.assertTrue(
            extract_gene_results(
                phen2gene_result=example_phen2gene_result,
                gene_identifier_updator=self.gene_identifier_updator,
            ).equals(
                pl.DataFrame(
                    [
                        {"gene_symbol": "GCDH", "gene_identifier": "ENSG00000105607", "score": 1.0},
                        {
                            "gene_symbol": "ETFB",
                            "gene_identifier": "ENSG00000105379",
                            "score": 0.298386,
                        },
                        {
                            "gene_symbol": "ETFA",
                            "gene_identifier": "ENSG00000140374",
                            "score": 0.286989,
                        },
                    ]
                )
            )
        )
