from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UsersViewSet, StoresViewSet, CustomTokenObtainPairView

app_name = "stores"

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'stores', StoresViewSet, basename='stores')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UsersViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]