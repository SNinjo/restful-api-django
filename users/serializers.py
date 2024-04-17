from users.models import User
from rest_framework_mongoengine.serializers import DocumentSerializer

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'name', 'age', 'created_at', 'updated_at')
