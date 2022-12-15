from django.contrib import admin

from .models import Genre, Category, Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'year',)
    list_filter = ('category',)
    list_editable = ('category', 'year',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'score', 'title', 'author')
    list_filter = ('pub_date',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'review', 'author')
    list_filter = ('pub_date',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
