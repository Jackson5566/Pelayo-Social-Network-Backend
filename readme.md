# API, parte de la web: Pelayo Social Network, así como de su proyecto

## Esta contruida con las siguientes tecnologias: DJANGO, DRF Y PYTHON

### Decoradores
La api trae consigo los siguientes decoradores para gestionar los diferentes procesos que su funcionalidades involucra
1. Decorador: get_posts (Se trata de un decorador que indica que la operación es de obtención de los posts creados y por lo tanto aplicara paginacion y serializacion a las clases que lo implementen )
2. Decorador: access_protected (Toda clase que implmente dicho controlador debe ser una vista, se le incorporará autenticacion por: JWT, solo tengan acceso los usuarios registrados)
3. Decorador: validate_serializer (Pide un serializer como parametro, a este se le aplicara la validación y en caso de fallar devolverá un error)

### Filosofía
Cuenta con clases para manejar las solicitudes de forma encapsulada, las logicas de las vistas son implmentadas en scripts separados, y dentro de la vista se debe crear una instancia de la clase que lleve dicha logica y retornar su respuesta: Para ello se cuenta con un shortcout: proccess_and_get_response. Ejemplo
@access_protected
class PostView(APIView):
    def get(self, request, _id):
        get_post_data_instance = GetPostData(post_id=_id, request=request)
        return process_and_get_response(get_post_data_instance)

### Generación de plantillas para llevar la logica de las Vistas
Dentro de la api existe un script llamado: "appgenerator.py", gracias a el podemos crear plantillas que nos faciliten la implementacion de la logica de las vistas extrayendo lo común.

