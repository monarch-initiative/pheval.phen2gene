from pathlib import Path

import click

from pheval_phen2gene.prepare.prepare_inputs import prepare_input, prepare_inputs


@click.command("prepare-input")
@click.option(
    "--phenopacket-path",
    "-p",
    required=True,
    metavar="FILE",
    help="Path to phenopacket.",
    type=Path
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    help="Path to output directory.",
    type=Path
)
def prepare_input_command(phenopacket_path: Path, output_dir: Path):
    prepare_input(phenopacket_path=phenopacket_path, output_dir=output_dir)


@click.command("prepare-inputs")
@click.option(
    "--phenopacket-dir",
    "-p",
    required=True,
    metavar="FILE",
    help="Path to phenopacket.",
    type=Path
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    help="Path to output directory.",
    type=Path
)
def prepare_inputs_command(phenopacket_dir: Path, output_dir: Path):
    prepare_inputs(phenopacket_dir=phenopacket_dir, output_dir=output_dir)
