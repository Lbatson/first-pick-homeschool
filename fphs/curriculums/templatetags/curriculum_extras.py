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


@register.inclusion_tag('reviews/star.html')
def star_rating(review):
    return {
        'stars': range(review.rating),
        'empty': range(5 - review.rating)
    }


@register.inclusion_tag('reviews/link.html', takes_context=True)
def review_link(context, curriculum):
    user = context['request'].user
    review = curriculum.reviews.filter(user__id=user.id).first() or None
    return {
        'curriculum': curriculum,
        'review': review
    }
