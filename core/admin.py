from django.contrib import admin
from .models import Profile, Post

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_user', 'name', 'surname', 'nationality')
    search_fields = ('user__username', 'name', 'surname')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'conditions', 'date_time')
    search_fields = ('user', 'title', 'id')
    list_filter = ('conditions', 'date_time')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
