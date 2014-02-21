from django import template

register = template.Library()

@register.filter
def format_phone(value):
	if value is None:
		return ""
	value = value.replace(" ", "").replace("-", "")
	value = value.replace("(", "").replace(")", "")
	if not value.isdigit():
		return value
	if len(value) == 9:
		return " ".join([value[0:3], value[3:6], value[6:9]])
	return value
