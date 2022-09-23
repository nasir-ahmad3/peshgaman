from django.contrib import admin
from .models import (
	Article, 
	Graph, 
	ArticleCategory, 
	GetIpAddress, 
	ArticleHit
)

# actions
def make_publish(ModelAdmin, request, queryset):
	queryset.update(status='p')
make_publish.short_description  = "انتشار مقالات انتخاب شده"


def make_draft(ModelAdmin, request, queryset):
	queryset.update(status='d')
make_publish.short_description  = "پیشنویس شدن  مقالات انتخاب شده"


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'position', 'slug', 'status']
	list_filter = ['position']
	prepopulated_fields = {'slug': ('title',)}
	search_fields = ('title', 'slug')
	ordering = ('position',)
admin.site.register(ArticleCategory, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'show_thumbnail', 'publish', 'status', 'category_to_str']
	list_filter = ['status', 'publish']
	ordering = ['-publish']
	search_fields = ('title', 'description')
	prepopulated_fields = {'slug': ('title',)}
	actions = ['make_publish', 'make_draft']
admin.site.register(Article, ArticleAdmin)


class GraphAdmin(admin.ModelAdmin):
	list_display = ['title',]
	list_filter = ['id']
	ordering = ['id']
	search_fields = ('title',)
admin.site.register(Graph, GraphAdmin)
admin.site.register(GetIpAddress)
admin.site.register(ArticleHit)