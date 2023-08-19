from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterApi


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterApi.as_view(), name='registration-view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientRetrieveUpdateDeleteView.as_view(), name='patient-retrieve-update-destroy'),
    path('users/', views.CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.CustomUserRetrieveUpdateDeleteView.as_view(), name='user-retrieve-update-destroy'),
]

