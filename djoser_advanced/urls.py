from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import CustomUserViewSet


router = DefaultRouter()

router.register("users", CustomUserViewSet, basename="user")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include(router.urls)),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
