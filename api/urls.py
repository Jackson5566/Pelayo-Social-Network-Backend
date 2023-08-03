from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/posts/', include("posts_app.urls")),
    path("api/message/", include("message_app.urls")),
    path('api/', include("users_app.urls")),
    path('api/', include("contact_app.urls")),
    path('api/', include("auth_app.urls")),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
]

if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)