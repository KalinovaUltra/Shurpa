from django.contrib import admin
from django.core.checks import messages
from django.utils.safestring import mark_safe

from .models import Shurpa, Category

class CalorieFilter(admin.SimpleListFilter):
    title="Калорийность"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('calorie', 'Калорийность'),
            ('nocalorie', 'Калорийности нет'),
        ]
    def queryset(self, request, queryset):
        if self.value() == 'calorie':
            return queryset.filter(calorie__isnull=False)
        elif self.value() == 'nocalorie':
            return queryset.filter(calorie__isnull=True)

@admin.register(Shurpa)
class ShurpaAdmin(admin.ModelAdmin):
    fields= ['title', 'content', 'photo', 'post_photo', 'slug', 'cat', 'tags']
    readonly_fields = ['slug', 'post_photo']
    filter_horizontal = ['tags']
    list_display = ('id', 'title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 12
    actions=['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [CalorieFilter, 'cat__name', 'is_published']

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, shurpa: Shurpa):
        if shurpa.photo:
            return mark_safe(f"<img src='{shurpa.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count= queryset.update(is_published= Shurpa.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикакции")
    def set_draft(self, request, queryset):
        count= queryset.update(is_published= Shurpa.Status.DRAFT)
        self.message_user(request, f"Изменено {count} записей снято с публикации.", messages.WARNING)

#admin.site.register(Shurpa, ShurpaAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
