from django import template

register = template.Library()

@register.filter
def search_include(value):
	base_dir = "search/includes/"
	content_types = [
		"crm.company",
		"crm.group",
	]
	if value is not None and value.content_type() in content_types:
		path = value.content_type().replace(".", "/")
		return "".join([base_dir, path, ".html"])


