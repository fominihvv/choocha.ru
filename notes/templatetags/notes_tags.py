from django import template
from django.db.models import Count, Q

from notes.models import Category, TagPost

register = template.Library()




@register.inclusion_tag('notes/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts', filter=Q(posts__is_published=True))).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('notes/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(total=Count('notes', filter=Q(notes__is_published=True))).filter(total__gt=0)
    return {'tags': tags}
