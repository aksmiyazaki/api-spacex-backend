import click
from config.configuration import Configuration

@click.command()
@click.option("--config_file", required=True, help="Configuration File Path.")
@click.option("--schema_file", help="Schema of the configuration File Path.", default="./resources/configs/config_schema.json")
def start(config_file, schema_file):
    return Configuration(config_file, schema_file)

if __name__ == '__main__':
    config = start()

