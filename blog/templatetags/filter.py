from django import template

register = template.Library()

@register.filter
def alt(value):
	if value % 2 == 1:
		return "alt"
	else:
		return "alttwo"

@register.filter
def num(value):
	return len(value)
