from django.urls import path
from .views import view_index, view_games_browser, initData

urlpatterns = [
    path('', view_index.index, name='main'),
    path('logout', view_index.disconnect, name='logout'),
    path('login', view_index.connect, name='login'),
    path('signIn', view_index.create_account, name='sign in'),
    path('confirm_email', view_index.verify_email, name="confirm_email"),
    path('reset', view_index.reset, name="reset"),
    path('confirm_reset', view_index.confirm_reset, name="confirm_reset"),
    path('games', view_games_browser.view_games, name="games"),

    path('init', initData.init_datas),
    path('test', view_index.test, name="test"),
    path('test2', view_index.test2, name="test2"),
]
