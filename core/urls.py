from django.urls import path
from . import views
from .views import user_profile

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
    path('logout/', views.logout, name="logout"),
    path('perTe/', views.perTe, name="perTe"),
    path('settings/', views.settings, name='settings'),
    path('create/', views.create, name='create'),
    path('edit/<uuid:post_id>', views.edit_post, name="edit_post"),
]