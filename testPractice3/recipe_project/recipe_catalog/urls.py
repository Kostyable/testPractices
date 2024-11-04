from django.conf.urls.static import static
from django.urls import path
from .views import about, index, recipe_detail
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe'),
    path('about/', about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)