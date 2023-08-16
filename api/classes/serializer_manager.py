class SerializerManager:
    """
    Clase controladora de los serializers
    Uso principal: Igual que otras se asegurará de el correcto manejo de los serilizers en las clases que la implementen
    """
    def __init__(self, serializer=None):
        self._serializer_class = serializer

    @property
    def serializer_class(self):
        return self._serializer_class

    @serializer_class.setter
    def serializer_class(self, serializer):
        self._serializer_class = serializer
