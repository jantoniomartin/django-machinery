from django.db.models.signals import post_migrate

def update_permissions_after_migration(app, **kwargs):
	"""
	Update app permission just after every migration.
	Taken from http://stackoverflow.com/questions/1742021/adding-new-custom-permissions-in-django
	"""
	from django.conf import settings
	from django.db.models import get_app, get_models
	from django.contrib.auth.management import create_permissions

	create_permissions(get_app(app), get_models(), 2 if settings.DEBUG else 0)

##TODO: FIX THIS
#post_migrate.connect(update_permissions_after_migration)
