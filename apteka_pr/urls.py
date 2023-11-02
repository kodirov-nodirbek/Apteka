from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


schema_view = get_schema_view(
   openapi.Info(
      title="Apteka API",
      default_version='v1',
      description="Apteka boshqaruvi uchun API",
      contact=openapi.Contact(email="nodirbek29@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path("auth/", include("rest_framework.urls")),
   path("dj-rest-auth/", include("dj_rest_auth.urls")),
   path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
   path('', include("dorixona_app.urls")),
   path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
