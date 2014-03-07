from om.models import CartItem

def cart_count(request):
	return {'cart_count': CartItem.objects.all().count() }
