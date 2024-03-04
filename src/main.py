import click
from config.configuration import Configuration
from controller.ingestion import IngestionController
from loader.file import FileLoader
from logger.boilerplate import get_logger
from sink.postgres import PostgresSink
from transformation.json_object import JSONObjectToListTransformer


@click.command()
@click.option("--config_file", required=True, help="Configuration File Path.")
@click.option("--schema_file", help="Schema of the configuration File Path.", default="./resources/configs/config_schema.json")
@click.option("--log_level", help="Log level.", default="INFO")
def start(config_file, schema_file, log_level):
    logger = get_logger(log_level)
    logger.info("Application Starting")

    config = Configuration(config_file, schema_file, logger)

    loader = FileLoader(config.configuration["input"]["input_file_path"],
                        config.configuration["input"]["input_file_schema_path"],
                        logger)
    loader.initialize_loader()

    sink = PostgresSink(config.configuration["postgres_sink_database"], logger=logger)

    json_to_list_transformation = JSONObjectToListTransformer(sink.fetch_insertion_fields_from_sql(),
                                                              config.configuration["object_to_list_transformation_mapping"])

    transformations = [json_to_list_transformation]

    ingestion_controller = IngestionController(loader, sink, transformations, logger)
    ingestion_controller.ingest()



if __name__ == '__main__':
    start()


