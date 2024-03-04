class JSONObjectToListTransformer:
    def __init__(self, elements_to_extract, extraction_mapping=None):
        self.__elements_to_extract = elements_to_extract
        self.__extraction_mapping = extraction_mapping

    def transform(self, json_object):
        extracted = []
        for element_name in self.__elements_to_extract:
            name_mapping = self.__find_element_by_column_name(element_name)
            mapped_json_element_name = name_mapping["json_object_name"] if name_mapping else element_name
            extracted.append(json_object[mapped_json_element_name])
        return extracted

    def __find_element_by_column_name(self, query_column_name):
        res = None
        if self.__extraction_mapping:
            res = next((mapping for mapping in self.__extraction_mapping if self.__extraction_mapping and mapping.get("query_column_name") == query_column_name), None)

        return res
