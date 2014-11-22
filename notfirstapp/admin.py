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
		

admin.site.register(Game,GameAdminConfig)
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