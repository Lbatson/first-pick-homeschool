from django import template

register = template.Library()


@register.simple_tag
def is_filtered(items, filterIds):
    return bool(set(map(lambda i: i.id, items)).intersection(filterIds))


@register.inclusion_tag("reviews/star.html")
def star_rating(rating):
    stars = range(int(rating))
    half = range(1 if rating % 1 >= 0.5 else 0)
    empty = range(5 - len(stars) - len(half))
    return {"stars": stars, "half": half, "empty": empty}


@register.inclusion_tag("reviews/link.html", takes_context=True)
def review_link(context, curriculum):
    user = context["request"].user
    review = curriculum.reviews.filter(user__id=user.id).first() or None
    return {"curriculum": curriculum, "review": review}
