from django import template

register = template.Library()


@register.simple_tag
def is_filtered(items, filterIds):
    return bool(set(map(lambda i: i.id, items)).intersection(filterIds))


@register.simple_tag(takes_context=True)
def url_replace(context, page):
    query = context['request'].GET.copy().urlencode()
    url = query.rpartition('&page=')[0] if '&page=' in query else query
    return f'{url}&page={page}'
