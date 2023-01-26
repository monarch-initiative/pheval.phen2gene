"""Phen2Gene Runner"""
from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner


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

    def post_process(self):
        """post_process"""
        print("post processing")
