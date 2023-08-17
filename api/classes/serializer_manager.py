class SerializerManager:
    """
    Clase controladora de los serializers
    Uso principal: Igual que otras se asegurará de el correcto manejo de los serilizers en las clases que la implementen
    """
    def __init__(self, serializer=None):
        self._serializer = serializer

    @property
    def serializer(self):
        return self._serializer

    @serializer.setter
    def serializer(self, serializer):
        self._serializer = serializer
