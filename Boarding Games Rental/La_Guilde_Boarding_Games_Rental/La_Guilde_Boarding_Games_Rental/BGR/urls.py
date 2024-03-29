from django.urls import path
from .views import view_index

urlpatterns = [
    path('', view_index.index, name='main'),
    path('logout', view_index.disconnect, name='logout'),
    path('login', view_index.connect, name='login'),
    path('signIn', view_index.create_account, name='sign in'),
    path('confirm_email', view_index.verify_email, name="confirm_email"),
    path('url2', view_index.index2, name='main2'),

]
