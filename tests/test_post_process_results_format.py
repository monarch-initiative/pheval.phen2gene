import unittest

import pandas as pd
from pheval.post_processing.post_processing import PhEvalGeneResult, RankedPhEvalGeneResult
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict

from pheval_phen2gene.post_process.post_process_results_format import (
    PhEvalGeneResultFromPhen2GeneTsvCreator,
    create_pheval_gene_result_from_phen2gene,
)

example_phen2gene_result = pd.DataFrame(
    [
        {"Rank": 1, "Gene": "GCDH", "ID": "2639", "Score": 1.0, "Status": "SeedGene"},
        {"Rank": 2, "Gene": "ETFB", "ID": "2109", "Score": 0.298386, "Status": "SeedGene"},
        {"Rank": 3, "Gene": "ETFA", "ID": "2108", "Score": 0.286989, "Status": "SeedGene"},
    ]
)


class TestPhEvalGeneResultFromPhen2GeneTsvCreator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phen2gene_result = PhEvalGeneResultFromPhen2GeneTsvCreator(
            phen2gene_tsv_result=example_phen2gene_result,
            gene_identifier_updator=GeneIdentifierUpdater(create_hgnc_dict(), "ensembl_id"),
        )

    def test_find_gene_symbol(self):
        self.assertEqual(
            self.phen2gene_result._find_gene_symbol(example_phen2gene_result.iloc[0]), "GCDH"
        )

    def test_find_ensembl_identifier(self):
        self.assertEqual(
            self.phen2gene_result._find_ensembl_identifier(example_phen2gene_result.iloc[0]),
            "ENSG00000105607",
        )

    def test_find_relevant_score(self):
        self.assertEqual(
            self.phen2gene_result._find_relevant_score(example_phen2gene_result.iloc[0]), 1.0
        )

    def test_extract_pheval_gene_requirements(self):
        self.assertEqual(
            self.phen2gene_result.extract_pheval_gene_requirements(),
            [
                PhEvalGeneResult(gene_symbol="GCDH", gene_identifier="ENSG00000105607", score=1.0),
                PhEvalGeneResult(
                    gene_symbol="ETFB", gene_identifier="ENSG00000105379", score=0.2984
                ),
                PhEvalGeneResult(
                    gene_symbol="ETFA", gene_identifier="ENSG00000140374", score=0.287
                ),
            ],
        )


class TestCreatePhEvalGeneResultFromPhen2Gene(unittest.TestCase):
    def test_create_pheval_gene_result_from_phen2gene(self):
        self.assertEqual(
            create_pheval_gene_result_from_phen2gene(
                example_phen2gene_result, GeneIdentifierUpdater(create_hgnc_dict(), "ensembl_id"), "descending"
            ),
            [
                RankedPhEvalGeneResult(
                    pheval_gene_result=PhEvalGeneResult(
                        gene_symbol="GCDH", gene_identifier="ENSG00000105607", score=1.0
                    ),
                    rank=1,
                ),
                RankedPhEvalGeneResult(
                    pheval_gene_result=PhEvalGeneResult(
                        gene_symbol="ETFB", gene_identifier="ENSG00000105379", score=0.2984
                    ),
                    rank=2,
                ),
                RankedPhEvalGeneResult(
                    pheval_gene_result=PhEvalGeneResult(
                        gene_symbol="ETFA", gene_identifier="ENSG00000140374", score=0.287
                    ),
                    rank=3,
                ),
            ],
        )
