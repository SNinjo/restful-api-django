from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.serializers import UserSerializer 
from users.models import User

swagger_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        'age': openapi.Schema(
            type=openapi.TYPE_INTEGER,
        ),
    }
)
swagger_response = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'age': openapi.Schema(
                type=openapi.TYPE_INTEGER,
            ),
            'created_at': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'updated_at': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
        }
    )
}

class UsersView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects().all() # type: ignore
        users_serializer = self.serializer_class(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

    @swagger_auto_schema(
        request_body=swagger_request_body,
        responses=swagger_response
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        except Exception as error:
            return JsonResponse({'error': str(error)}, safe=False)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=swagger_request_body,
        responses=swagger_response
    )
    def patch(self, request, *args, **kwargs):
        user = User.objects(id=request.query_params['id']).first() # type: ignore
        if user:
            try:
                serializer = self.serializer_class(user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            except Exception as error:
                return JsonResponse({'error': str(error)}, safe=False)
        else:
            return JsonResponse(None, safe=False)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=swagger_request_body,
        responses=swagger_response
    )
    def put(self, request, *args, **kwargs):
        user = User.objects(id=request.query_params['id']).first() # type: ignore
        if user:
            try:
                serializer = self.serializer_class(user, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            except Exception as error:
                return JsonResponse({'error': str(error)}, safe=False)
        else:
            return JsonResponse(None, safe=False)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ],
        responses=swagger_response
    )
    def delete(self, request, *args, **kwargs):
        user = User.objects(id=request.query_params['id']).first() # type: ignore
        if user:
            users_serializer = self.serializer_class(user)
            user.delete()
            return JsonResponse(users_serializer.data, safe=False)
        else:
            return JsonResponse(None, safe=False)
