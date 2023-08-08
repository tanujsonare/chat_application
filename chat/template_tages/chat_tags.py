from django import template

register = template.Library()

@register.filter(name="initials")
def initials(value):
    initials = ""
    for name in value.split(" "):
        if name:
            initials += name[0].upper()

    return initials