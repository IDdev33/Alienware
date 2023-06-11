
from django import template

register = template.Library()

@register.simple_tag
def star_rating(score, max_rating=5):
    score = float(score)
    full_stars = int(score)
    half_star = score - full_stars >= 0.5
    empty_stars = max_rating - full_stars - half_star

    stars = []
    for _ in range(full_stars):
        stars.append('full')
    if half_star:
        stars.append('half')
    for _ in range(empty_stars):
        stars.append('empty')

    return {'stars': stars}





