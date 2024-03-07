from logging import INFO


class IngestionController:
    def __init__(self, loader, sink, transformations, logger=None):
        self.__loader = loader
        self.__sink = sink
        self.__transformations = transformations
        self.__logger = logger

    def __log_if_set(self, msg, level=INFO):
        if self.__logger:
            self.__logger.log(level, msg)

    def ingest(self):
        loaded_object = self.__loader.load_object_based_on_schema()
        self.__log_if_set("Starting loading data.")
        while loaded_object is not None:
            transformed_object = self.__apply_all_transformations_on_object(loaded_object)
            self.__sink.insert_object(transformed_object)
            loaded_object = self.__loader.load_object_based_on_schema()
        self.__log_if_set("Finished loading data, commiting....")
        self.__sink.commit_changes()
        self.__log_if_set("Changes Commited.")

    def __apply_all_transformations_on_object(self, json_object):
        def __apply_transformation(input, transformation_list):
            if transformation_list:
                transformed_object = transformation_list[0].transform(input)
                return __apply_transformation(transformed_object, transformation_list[1:])
            else:
                return input

        return __apply_transformation(json_object, self.__transformations)
