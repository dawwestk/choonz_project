from django.contrib import admin
from choonz.models import Playlist, UserProfile

# Register your models here.

class PlaylistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'creator', 'createdDate',) # 'averageRating')

#class PageAdmin(admin.ModelAdmin):
#    list_display = ('title', 'playlist', 'url')

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(UserProfile)