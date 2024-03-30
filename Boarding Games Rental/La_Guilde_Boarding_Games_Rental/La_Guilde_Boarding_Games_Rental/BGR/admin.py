from django.contrib import admin
from .models import User, Genre, Game, Command, FavCommand

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Command)
admin.site.register(FavCommand)
