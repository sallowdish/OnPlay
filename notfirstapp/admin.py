from django.contrib import admin
from notfirstapp.models import *

# Register your models here.
class GameAdminConfig(admin.ModelAdmin):
	"""docstring for GameAdmin"""
	list_display=('gamename','createTime')

# class AccountAdminConfig(admin.ModelAdmin):
# 	list_display=('username','firstname','lastname','isGameDeveloper')

@admin.register(GameArchive)
class GameArchiveAdmin(admin.ModelAdmin):
	"""docstring for GameArchiveAdmin"""
	list_display=('name','gamefile','upload_time')

#blog	
class BlogAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
	

admin.site.register(Game,GameAdminConfig)
admin.site.register(SpotlightGame)
# admin.site.register(Account,AccountAdminConfig)
admin.site.register(Play)
admin.site.register(Own)
admin.site.register(ScoreRank)
admin.site.register(TimeRank)
admin.site.register(Figure)
admin.site.register(Image)
admin.site.register(GameComment)
admin.site.register(GameRate)
admin.site.register(OnPlayUser)
#blog
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
