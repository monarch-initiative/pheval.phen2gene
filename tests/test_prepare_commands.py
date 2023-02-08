import os
import unittest
from pathlib import Path

from pheval_phen2gene.prepare.prepare_commands import (
    Phen2GeneCommandLineArguments,
    Phen2GeneDockerArguments,
    create_command_line_arguments,
    create_docker_arguments,
)


class TestCreateCommandLineArguments(unittest.TestCase):
    def test_create_command_line_arguments_input_file(self):
        self.assertEqual(
            create_command_line_arguments(
                path_to_phen2gene_dir=Path("/path/to/phen2gene.py"),
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=Path("/path/to/input.txt"),
                phenopacket_path=None,
            ),
            Phen2GeneCommandLineArguments(
                path_to_phen2gene_dir=Path("/path/to/phen2gene.py"),
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=Path("/path/to/input.txt"),
                hpo_ids=None,
            ),
        )

    def test_create_command_line_arguments_phenopacket(self):
        self.assertEqual(
            create_command_line_arguments(
                path_to_phen2gene_dir=Path("/path/to/phen2gene.py"),
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=None,
                phenopacket_path=Path(os.path.dirname(__file__)).joinpath(
                    "input_dir/phenopacket.json"
                ),
            ),
            Phen2GeneCommandLineArguments(
                path_to_phen2gene_dir=Path("/path/to/phen2gene.py"),
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=None,
                hpo_ids=["HP:0000256", "HP:0000486"],
            ),
        )


class TestCreateDockerArguments(unittest.TestCase):
    def test_create_docker_arguments_input_file(self):
        self.assertEqual(
            create_docker_arguments(
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=Path("/path/to/input.txt"),
                phenopacket_path=None,
            ),
            Phen2GeneDockerArguments(
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=Path("/path/to/input.txt"),
                hpo_ids=None,
            ),
        )

    def test_create_docker_arguments_phenopacket(self):
        self.assertEqual(
            create_docker_arguments(
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=None,
                phenopacket_path=Path(os.path.dirname(__file__)).joinpath(
                    "input_dir/phenopacket.json"
                ),
            ),
            Phen2GeneDockerArguments(
                output_dir=Path("/path/to/output_dir"),
                output_file_name="output_file.txt",
                input_file_path=None,
                hpo_ids=["HP:0000256", "HP:0000486"],
            ),
        )
