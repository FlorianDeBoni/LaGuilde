from django.urls import path
from .views import view_index, view_games_browser, view_favorites, view_borrow, view_favcommand

urlpatterns = [
    path('', view_index.index, name='main'),
    path('logout', view_index.disconnect, name='logout'),
    path('login', view_index.connect, name='login'),
    path('signIn', view_index.create_account, name='sign in'),
    path('confirm_email', view_index.verify_email, name="confirm_email"),
    path('reset', view_index.reset, name="reset"),
    path('confirm_reset', view_index.confirm_reset, name="confirm_reset"),
    path('games', view_games_browser.view_games, name="games"),
    path('favorites', view_favorites.favorites, name="favorites"),
    path('borrow', view_borrow.borrowform, name="borrow"),
    path('borrow/delete', view_borrow.delete, name="delete"),
    path('borrow/fav', view_borrow.add_fav_command, name="fav"),
    path('borrow/<int:id>', view_favcommand.fav_command, name="command"),
    path('erase/<int:id>', view_favcommand.del_fav_command, name="erase"),
    path('change', view_index.change_language, name="change"),

]
