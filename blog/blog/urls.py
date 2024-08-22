from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from post import views


urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/register/', views.RegistrationView.as_view(), name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),
      name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('post.urls', namespace='post')),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
