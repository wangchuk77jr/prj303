from django.urls import path
from . import views

urlpatterns = [
    path('artist/login',views.Login,name='login'),
    path('artist/signup',views.Signup,name='signup'),
    path('artist/userdashboard',views.UserDashboard,name='userdashboard'),
    path('artist/token_send', views.Token_send, name='token'),
    path('artist/success', views.Success, name='success'),
    path('artist/verify/<auth_token>', views.Verify, name='verify'),
    path('artist/error', views.Error, name='error'),
    path('artist/my_music',views.My_Music, name='myMusic'),
    path('artist/upload_music',views.Upload_Music, name='uploadMusic'),
    path('artist/profile_setting',views.SettingProfile,name='profile_setting'),
    path('logout/', views.logout_view, name='logout'),

   
]