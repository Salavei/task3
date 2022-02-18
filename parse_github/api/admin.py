from django.contrib import admin
from .models import GitItem, GitUser

admin.site.site_header = 'Парсинг Гитов'


@admin.register(GitItem)
class GitItemItemAdmin(admin.ModelAdmin):
    pass


@admin.register(GitUser)
class GitUserAdmin(admin.ModelAdmin):
    pass
