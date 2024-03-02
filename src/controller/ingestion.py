class IngestionController:
    def __init__(self, loader, sink):
        self.__loader = loader
        self.__sink = sink
