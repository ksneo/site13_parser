import click
import os
from proccess_xml import proccess_xml


@click.command()
@click.argument('file')
def main(file):
    """
    1C site13 dictionary parser
    """
    if not os.path.isfile(file):
        click.echo(f"File not exists {file}")
        exit(1)

    with open(file, mode="r", encoding="utf-8") as xml_file:
        result = proccess_xml(xml_file)
        click.echo(result)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()