from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from account.views import CreateAuthorAPIView
from news import views

schema_view = get_schema_view(
   openapi.Info(
      title="Exam API",
      default_version='v0.1',
      description="API для новостей",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/register/', CreateAuthorAPIView.as_view()),
    path('api/account/', include('rest_framework.urls')),
    path('api/account/token/', obtain_auth_token),
    path('api/account/token/', obtain_auth_token),
    path('api/news/', views.NewsCreateListAPIView.as_view(), name='news'),
    path('api/news/<int:pk>/', views.NewsUpdateDestroyAPIView.as_view(), name='news_up'),
    path('api/news/<int:pk>/comments/', views.CommentListCreateAPIView.as_view(), name='comment'),
    path('api/news/<int:pk>/comments/<int:id>/', views.CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment_up'),
    path('api/statuses/', views.StatusListCreateAPIView.as_view(), name='status'),
    path('api/statuses/<int:pk>', views.StatusRetrieveUpdateDestroyAPIView.as_view(), name='status_up'),
    #path('api/news/<int:pk>/<slug>/', views.status_add_to_news, name='slu_news'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),
]
