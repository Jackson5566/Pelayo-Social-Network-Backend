from auth_app.models import User
from api.serializers import DynamicModelSerializer

class UsersSerializerReturn2(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'description', 'email', 'id', 'isProfessor']