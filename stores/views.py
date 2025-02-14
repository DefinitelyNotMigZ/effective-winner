from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Users,Stores
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StoreSerializer, UserSerializer, CustomTokenObtainPairSerializer


# class LoginAPIView(APIView):
#     serializer_class =
#     permission_classes = []

#     def post(self, request):
#         pass
#     def get(self, request):
#         pass

class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        path = self.request.path

        if "register" in path:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoresViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Stores.objects.all()
    serializer_class = StoreSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
