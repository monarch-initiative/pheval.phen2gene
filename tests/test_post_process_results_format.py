import unittest

import pandas as pd
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict

from pheval_phen2gene.post_process.post_process_results_format import StandardisePhen2GeneResult


class TestStandardisePhen2GeneResult(unittest.TestCase):
    result = None

    @classmethod
    def setUpClass(cls) -> None:
        hgnc_dict = create_hgnc_dict()
        gene_identifier_updater = GeneIdentifierUpdater(hgnc_dict, "ensembl_id")
        cls.result = [
            {"Rank": 1, "Gene": "GCDH", "ID": "2639", "Score": 1.0, "Status": "SeedGene"},
            {"Rank": 2, "Gene": "ETFB", "ID": "2109", "Score": 0.298386, "Status": "SeedGene"},
            {"Rank": 3, "Gene": "ETFA", "ID": "2108", "Score": 0.286989, "Status": "SeedGene"},
        ]
        cls.standardise_result = StandardisePhen2GeneResult(
            gene_result=pd.DataFrame(cls.result), gene_identifier_updater=gene_identifier_updater
        )
        cls.standardised_result = []

    def test_add_ensembl_identifier(self):
        self.assertEqual(
            self.standardise_result.add_ensembl_identifier(("GCDH")), "ENSG00000105607"
        )

    def test_create_result_dictionary(self):
        self.assertEqual(
            self.standardise_result.create_result_dictionary(pd.Series(self.result[0])),
            {"gene_symbol": "GCDH", "gene_identifier": "ENSG00000105607", "score": 1.0},
        )

    def test_simplify_result(self):
        self.assertEqual(
            self.standardise_result.simplify_result(self.standardised_result),
            [
                {"gene_symbol": "GCDH", "gene_identifier": "ENSG00000105607", "score": 1.0},
                {"gene_symbol": "ETFB", "gene_identifier": "ENSG00000105379", "score": 0.2984},
                {"gene_symbol": "ETFA", "gene_identifier": "ENSG00000140374", "score": 0.287},
            ],
        )

    def test_sort_result(self):
        self.assertEqual(
            self.standardise_result.sort_result(
                [
                    {"gene_symbol": "GCDH", "gene_identifier": "ENSG00000105607", "score": 1.0},
                    {"gene_symbol": "ETFB", "gene_identifier": "ENSG00000105379", "score": 0.2984},
                    {"gene_symbol": "ETFA", "gene_identifier": "ENSG00000140374", "score": 0.287},
                ]
            ),
            [
                {"gene_symbol": "GCDH", "gene_identifier": "ENSG00000105607", "score": 1.0},
                {"gene_symbol": "ETFB", "gene_identifier": "ENSG00000105379", "score": 0.2984},
                {"gene_symbol": "ETFA", "gene_identifier": "ENSG00000140374", "score": 0.287},
            ],
        )

    def test_add_ranks(self):
        self.assertEqual(
            self.standardise_result.add_ranks(
                [
                    {"gene_symbol": "GCDH", "gene_identifier": "ENSG00000105607", "score": 1.0},
                    {"gene_symbol": "ETFB", "gene_identifier": "ENSG00000105379", "score": 0.2984},
                    {"gene_symbol": "ETFA", "gene_identifier": "ENSG00000140374", "score": 0.287},
                ]
            ),
            [
                {
                    "gene_symbol": "GCDH",
                    "gene_identifier": "ENSG00000105607",
                    "score": 1.0,
                    "rank": 1,
                },
                {
                    "gene_symbol": "ETFB",
                    "gene_identifier": "ENSG00000105379",
                    "score": 0.2984,
                    "rank": 2,
                },
                {
                    "gene_symbol": "ETFA",
                    "gene_identifier": "ENSG00000140374",
                    "score": 0.287,
                    "rank": 3,
                },
            ],
        )

    def test_standardise_gene_result(self):
        self.assertEqual(
            self.standardise_result.standardise_gene_result(),
            [
                {
                    "gene_symbol": "GCDH",
                    "gene_identifier": "ENSG00000105607",
                    "score": 1.0,
                    "rank": 1,
                },
                {
                    "gene_symbol": "ETFB",
                    "gene_identifier": "ENSG00000105379",
                    "score": 0.2984,
                    "rank": 2,
                },
                {
                    "gene_symbol": "ETFA",
                    "gene_identifier": "ENSG00000140374",
                    "score": 0.287,
                    "rank": 3,
                },
            ],
        )
