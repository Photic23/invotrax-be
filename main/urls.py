from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
app_name = 'main'

urlpatterns = [
    # Your other URLs
    path('test-db-connection/', views.test_db_connection, name='test_db_connection'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),
    
    
    # User management endpoints
    path('admins/users/', views.UserManagementView.as_view(), name='user_list'),
    path('admins/users/<int:user_id>/', views.UserManagementView.as_view(), name='user_detail'),
    path('admins/users/<int:user_id>/permissions/', views.CustomPermissionView.as_view(), name='user_permissions'),

    # New endpoints for soft delete functionality
    path('admins/users/<int:user_id>/restore/', views.UserRestoreView.as_view(), name='user_restore'),
    path('admins/users/<int:user_id>/restore/', views.UserRestoreView.as_view(), name='user_restore'),
    path('admins/users/<int:user_id>/hard-delete/', views.UserHardDeleteView.as_view(), name='user_hard_delete'),
]