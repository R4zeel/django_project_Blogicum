from django.contrib import admin
from django.contrib.auth import admin as user_admin

from .models import Category, Location, Post

# Разделил админки постов и категорий, так как параметр
# фильтрации по pub_date недоступен для модели категорий,
# происходил конфликт. Также добавил фильтры по локациям
# и категориям, но на панели админки они
# отображаются как object(1) и т.п. Общие is_published и
# created_at пытался вынести в один класс родителя, но не понял,
# как добавлять к ним другие значения в дочерних классах.
# Метод .append() на параметры админки не работал

admin.site.empty_value_display = 'Пусто'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_published',
        'created_at',
        'pub_date',
        'category'
    ]
    list_editable = [
        'is_published',
        'pub_date'
    ]
    list_filter = [
        'is_published',
        'pub_date',
        'location',
        'category'
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_published',
        'created_at'
    ]
    list_editable = ['is_published']
    list_filter = ['is_published']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_published',
        'created_at'
    ]
    list_editable = ['is_published']


class UserAdmin(user_admin.UserAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_published',
        'created_at'
    ]
    list_editable = ['is_published']
