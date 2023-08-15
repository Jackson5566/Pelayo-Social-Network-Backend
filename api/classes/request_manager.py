class RequestManager:
    """Clase controladora o encapsuladora de las solicitudes
    Uso principal: Controlar las solicitudes para que las clases que la implementen pueda manipularlas correctamente"""
    def __init__(self, request):
        self._request = request

    @property
    def request(self):
        return self._request

    def __str__(self):
        return self.request
