from django.urls import path, include
from django.conf import settings

from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views

router = DefaultRouter()
router.APIRootView = APIRootView
router.register('users', views.UserViewSet, basename='user')
router.register('tasks', views.TaskViewSet, basename='task')
router.register('tags', views.TagViewSet, basename='tag')
router.register('projects', views.ProjectViewSet, basename='project')

app_name = 'main'
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/uuid/', views.RegisterUUIDView.as_view()),
    path('api/register/user/', views.RegisterUserView.as_view()),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),
    path('api/auth/uuid/', views.AuthUUIDView.as_view()),
    path('api/auth/user/', obtain_jwt_token),
    path('api/user/', views.UserView.as_view()),
]

if settings.DEBUG:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="API Schema",
            default_version='v1',
            description="",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    urlpatterns.extend([
        path('api/register/dummy/', views.RegisterDummyUserView.as_view()),
        path('schema/',
             schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
    ])
