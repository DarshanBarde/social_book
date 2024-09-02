from django.urls import path
from . import views
from .views import Register,Login,Home,MyBooksView
from .views import logout,authors_and_sellers
from .views import MyView,LoginView,FileAPI



urlpatterns=[
    path('register',Register.as_view(),name='register'),
    path('login',Login.as_view(),name='login'),
    path('logout',logout,name='logout'),
    path('home',Home.as_view(),name='home'),
    path('mybook',MyBooksView.as_view(),name='mybook'),
    path('authnsell',authors_and_sellers,name='authnsell'),
    path('mydata',MyView.as_view(),name='mydata'),
    path('api/files/', FileAPI.as_view()),
    path('api/login/', LoginView.as_view(), name='login_api'),
    
]