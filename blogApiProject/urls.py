from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.api.urls')),
    path('', include('blog.api.urls')),
]
