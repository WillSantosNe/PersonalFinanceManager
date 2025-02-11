from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views
from accounts.views import UserViewSet
from transactions.views import TransactionViewSet
from reports.views import ReportViewSet
from categories.views import CategoryViewSet
from goals.views import GoalViewSet
from dashboard.views import DashboardViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'goals', GoalViewSet, basename='goals')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login JWT
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
    path('api/', include(router.urls)),
]
