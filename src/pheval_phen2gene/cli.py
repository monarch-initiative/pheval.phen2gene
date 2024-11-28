import click

from pheval_phen2gene.cli_phen2gene import prepare_commands_command, prepare_inputs_command


@click.group()
def main():
    pass


main.add_command(prepare_inputs_command)
main.add_command(prepare_commands_command)

if __name__ == "__main__":
    main()
