from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import about, index, recipe_detail, create_recipe, edit_recipe, delete_recipe, create_ingredient, signup
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe'),
    path('about/', about, name='about'),
    path('recipe/create/', create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/edit/', edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', delete_recipe, name='delete_recipe'),
    path('recipe/<int:pk>/create_ingredient/', create_ingredient, name='create_ingredient'),
    path('login/', LoginView.as_view(template_name='recipe_catalog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)