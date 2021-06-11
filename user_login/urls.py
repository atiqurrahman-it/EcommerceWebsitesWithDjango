from django.urls import path
from .import views
app_name = 'user_login'
urlpatterns = [
     path('sing_up/',views.Sing_up,name='sing_up'),
     path('login/',views.login_page,name='login'),
     path('logout/',views.Log_out,name='logout'),
     path('E_profile/',views.user_profile_edit,name='edit_profile'),

]