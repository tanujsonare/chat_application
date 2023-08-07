from django import template

register = template.Library()

@register.filter(name="initials")
def initials(value):
    initials = ""
    # breakpoint()
    for name in value.split(" "):
        if name and len(name) < 3:
            initials += name[0].upper()

    return initials