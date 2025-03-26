"""Phen2Gene Runner"""

from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_phen2gene.post_process.post_process import post_process_results_format
from pheval_phen2gene.run.run import prepare_phen2gene_commands, run_phen2gene
from pheval_phen2gene.tool_specific_configuration_parser import Phen2GeneToolSpecificConfigurations


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
        tool_specific_configurations = Phen2GeneToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        prepare_phen2gene_commands(
            config=tool_specific_configurations,
            tool_input_commands_dir=self.tool_input_commands_dir,
            testdata_dir=self.testdata_dir,
            data_dir=self.input_dir,
            raw_results_dir=self.raw_results_dir,
        )
        run_phen2gene(
            config=tool_specific_configurations,
            testdata_dir=self.testdata_dir,
            input_dir=self.input_dir,
            raw_results_dir=self.raw_results_dir,
            tool_input_commands_dir=self.tool_input_commands_dir,
        )

    def post_process(self):
        """post_process"""
        print("post processing")
        tool_specific_configurations = Phen2GeneToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        post_process_results_format(
            raw_results_dir=self.raw_results_dir,
            output_dir=self.output_dir,
            phenopacket_dir=self.testdata_dir.joinpath("phenopackets"),
            config=tool_specific_configurations,
        )
