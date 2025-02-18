from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Users, Stores
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    StoreSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)


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

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoresViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer

    def get_queryset(self):
        # return stores created by the current user
        return Stores.objects.filter(user=self.request.user)

    def create(self, request):
        data = request.data
        user = request.user  # get user obj stored in request via login

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        store_name = validated_data.get("store_name")

        existing_store = Stores.objects.filter(store_name__iexact=store_name)

        if existing_store:
            return Response(
                {"detail": "A store with the same name already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data["user"] = user

        created_store = Stores.objects.create(**validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # permission sa store
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # check if owner
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # delete ng store
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this store."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
