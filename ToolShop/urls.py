from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from catalog.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='catalog/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)