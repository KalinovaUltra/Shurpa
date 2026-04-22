from django import template
import shurpa.views as views
from shurpa.models import Category, TagPost

register= template.Library()


@register.inclusion_tag('shurpa/list_categories.html')
def show_categories(cat_selected_id=0):
        cats = Category.objects.all()
        return {'cats': cats, 'cat_selected': cat_selected_id}

@register.inclusion_tag('shurpa/list_tags.html')
def show_all_tags():
        return {'tags': TagPost.objects.all()}

