from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Users,Stores
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StoreSerializer, UserSerializer, CustomTokenObtainPairSerializer

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
    serializer_class = StoreSerializer

    def get_queryset(self):
        # return stores created by the current user
        return Stores.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # set yung user na nag create ng store
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # permission sa store
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this store."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # check if owner
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this store."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # delete ng store
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this store."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['delete'])
    def delete_store(self, request, pk=None):
        try:
            store = self.get_object()
            if store.user != request.user:
                return Response(
                    {"detail": "You do not have permission to delete this store."},
                    status=status.HTTP_403_FORBIDDEN
                )
            store.delete()
            return Response(
                {"detail": "Store deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Stores.DoesNotExist:
            return Response(
                {"detail": "Store not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
