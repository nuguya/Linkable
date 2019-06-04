from django.urls import path
from myapp import views
from .views import RegistrationAPI
#from rest_framework.authtoken import views

urlpatterns = [
    path('login', views.login),
    path('register', RegistrationAPI.as_view()),
    path('best',views.book_list),
    path('book/<int:pk>',views.select_book),
    path('mybook',views.my_book),
    path('rank',views.recommend_book),
]