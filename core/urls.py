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
    path('edit/<uuid:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path('follow/<int:user_id>/', views.follow_function, name="follow_function"),
    path('like/<uuid:post_id>/', views.like_function, name="like_function"),
    path('wishlist/<uuid:post_id>/', views.wishlist_function, name="wishlist_function"),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]