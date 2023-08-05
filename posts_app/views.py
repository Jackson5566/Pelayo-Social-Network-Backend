from .models import PostModel
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from .serializer import PostsCreateSerializer, PostsReturnSerializerWithUser, PostsReturnSerializerWithoutUser, FilesSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from necesary_scripts.list_features import sort, separate_by_vowels
from necesary_scripts.search_requirements import delete_repetitive_characters, Coincidences
from rest_framework.views import APIView
from .paginations import MyPagination
from rest_framework import viewsets
from .models import CategoryModel
from api.serializers import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import FileModel

class PostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, _id, format=None):
        posts = PostModel.objects.get(id=_id)
        context = {'request': request }

        if self.request.query_params.get('onlyMessages') == 'true':
            posts_serializer = PostsReturnSerializerWithoutUser(posts, many=False, context=context, fields=['messages'])
            return Response(posts_serializer.data)
        else:
            if posts.user == request.user:
                posts_serializer = PostsReturnSerializerWithoutUser(posts, many=False, context=context)
                fromUser = True
            else:
                posts_serializer = PostsReturnSerializerWithUser(posts, many=False, context=context)
                fromUser = False

            info = posts_serializer.data
            info['fromUser'] = fromUser
            return Response(info)

    def post(self, request, format=None):
        # file_serializer = FilesSerializer(data=request.data)
        files_instances = self.serialize_files(request)

        posts_serializer = PostsCreateSerializer(data=request.data)
        if posts_serializer.is_valid():
            post_instance = posts_serializer.create(validated_data=posts_serializer.validated_data, user=request.user)

            self.add_files(files_instances=files_instances, post_instance=post_instance)

            self.setCategories(request=request, instance=post_instance)

            return Response({
                'message': 'Exito con la creación'
            }, status=status.HTTP_201_CREATED)
        
        return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, _id):
        post = PostModel.objects.get(id=_id)
        post.delete()
        return Response({'message': 'Delete'}, status=status.HTTP_200_OK)


    def put(self, request, format=None):
        posts_serializer = PostsCreateSerializer(data=request.data)

        files_instances = self.serialize_files(request=request)

        if posts_serializer.is_valid():
            post = PostModel.objects.get(id=request.data['id'])

            post.categories.clear()

            self.setCategories(request=request, instance=post)

            if (request.user == post.user):
                post_instance = posts_serializer.update(validated_data=posts_serializer.validated_data, instance=post)

                self.add_files(post_instance=post_instance, files_instances=files_instances)

                return Response({
                    'message': 'Exito con la actualización'
                }, status=status.HTTP_200_OK)
            return Response({
                    'message': 'No tienes permiso para realizar la actualización'
                }, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'message': 'Error con la actualización, información no válida'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, _id):
        posts = PostModel.objects.get(id=_id)
        likes_user = request.user in posts.likes.all()
        disslikes_user = request.user in posts.disslikes.all()

        likes = request.data['likes']
        disslikes = request.data['disslikes']

        if (request.data['like']):
            if (likes_user):
                posts.likes.remove(request.user)
                likes -= 1
            else:
                posts.likes.add(request.user)
                likes += 1

            if (disslikes_user):
                posts.disslikes.remove(request.user)
                disslikes -= 1

        else: 
            if (disslikes_user):
                posts.disslikes.remove(request.user)
                disslikes -= 1
            else:
                posts.disslikes.add(request.user)
                disslikes += 1

            if (likes_user):
                posts.likes.remove(request.user)
                likes -= 1
        
        return Response({
            "likes": likes,
            "disslikes": disslikes
        }, status=status.HTTP_200_OK)
    
    def setCategories(self, instance, request):
        for category in request.data.getlist('categories'):
            category_instance = CategoryModel.objects.filter(name=category).first()
            if category_instance:
                instance.categories.add(category_instance)

    def serialize_files(self, request):
        file_serializer = FilesSerializer(data=request.data)

        if file_serializer.is_valid():
            files_instances = file_serializer.create(validated_data=file_serializer.validated_data)
        else: 
            files_instances = None
        
        return files_instances
    
    def add_files(self, files_instances, post_instance):
        if files_instances:
            for file in files_instances:
                post_instance.files.add(file)


class PostsViewSet(generics.ListAPIView):
    serializer_class = PostsReturnSerializerWithUser
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories__name']

    def get_queryset(self):
        return PostModel.objects.all().order_by('-created')

class SearchViewSet(viewsets.ModelViewSet):
    permission_classes =[permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPagination
    serializer_class = PostsReturnSerializerWithUser

    def get_queryset(self):
        # Tomamos la informacion recibida mediante el HttpParams de Angular, que contiene la búsqueda realizada
        search = self.request.query_params.get('search')
        # Eliminamos los espacios de la cadena de texto. Convertimos el texo a lowercase para evitar problemas en cuanto igualdad
        search = search.strip().lower()

        # Se separa la cadena de texto por vocales mediante la funcion creada por mi de separate_by_vowels
        search = separate_by_vowels(search)
        # Para ahorranos coincidencias inecesarias eliminamos los caracteres que son iguales
        search = list(set(search))

        # Se crea una lista para añadir posteriormente en ella los elementos de la base de datos y sus coincidencias
        list_coincidence = []

        # Exploramos todos los posts que hay dentro de la vase de datos
        for element in PostModel.objects.all().order_by("-created"):
            # Separamos por vocales la descripcion de los elementos
            list_content = separate_by_vowels(element.description.lower())
            # Separamos por vocales el titulo de los elementos
            list_title = separate_by_vowels(element.title.lower())
            # Almacenamos las coincidencias totales y hacemos uso para ello de la funcion Coincidence
            coincidences = (Coincidences(list_title, search) + Coincidences(list_content, search))
            #Comprobamos si las coincidencias son mayores a 0, si es así vamos a tener en cuenta estos elementos
            if coincidences > 0: list_coincidence.append([coincidences, element])

        # Gracias a la creacion del array bidimensional podemos ordenar la lista
        # sort(list=list_coincidence, reverse=True)
        list_coincidence.sort(key=lambda element: element[0], reverse=True)
        
        # Para devolver algo limpio, debemos de eliminar la estrategia del array bidimension que se utlizó
        list_unidimensional = [element[1] for element in list_coincidence]

        # Devolvemos una respuesta con los elementos sin sus respectivas coincidencias

        """EL algoritmo se basa en separar lo esrito por vocales, de esta forma logramos una busqueda mucho mas efectiva mirando la
        semejanza de las palabras. Ejemplo: Coche, cole. Estas palabras guardan cierta semejanza, y queremos ser concientes de esta
        semejanza """

        return list_unidimensional

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def pre_search(request):
    title_posts = [post.title for post in PostModel.objects.all()]
    return Response(title_posts)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_categories(request):
    categories = CategoryModel.objects.all()
    serialized_categories = CategorySerializer(categories, many=True)
    return Response(serialized_categories.data)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_file(request, id):
    try:
        file = FileModel.objects.get(id=id)
        file.delete()
        return Response({
            'message': 'Recurso eliminado con éxito'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'message': 'Recurso no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
