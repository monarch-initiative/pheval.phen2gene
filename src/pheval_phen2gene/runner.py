"""Phen2Gene Runner"""
from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_phen2gene.post_process.post_process import post_process_results_format
from pheval_phen2gene.run.run import prepare_phen2gene_commands, run_phen2gene
from pheval_phen2gene.utils.phen2gene_config_parser import parse_phen2gene_config


@dataclass
class Phen2GenePhEvalRunner(PhEvalRunner):
    """_summary_"""

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path

    def prepare(self):
        """prepare"""
        print("preparing")

    def run(self):
        """run"""
        print("running with phen2gene")
        config = parse_phen2gene_config(self.config_file)
        prepare_phen2gene_commands(
            config=config,
            output_dir=self.output_dir,
            testdata_dir=self.testdata_dir,
            data_dir=self.input_dir,
        )
        run_phen2gene(
            config=config,
            testdata_dir=self.testdata_dir,
            output_dir=self.output_dir,
            input_dir=self.input_dir,
        )

    def post_process(self):
        """post_process"""
        print("post processing")
        post_process_results_format(testdata_dir=self.testdata_dir, output_dir=self.output_dir)
