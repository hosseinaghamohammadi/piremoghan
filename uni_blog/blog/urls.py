from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'blog', views.StudentView, 'blog')


app_name = 'blog'

urlpatterns = [
    ################################################ arbitrary users
    path('', views.SignUpView.as_view(), name='signup'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('login/', views.user_login, name='login'),
        path('logout/', views.user_logout, name='logout'),

    ################################################ authorized users

    path('feed/', views.Feed.as_view(), name='feed'),
    path('edit_profile/', views.Profile.as_view(), name='profile'),
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('edit_post/', views.EditPost.as_view(), name='edit_post'),
    # path('create/', views.QuillPostCreateView.as_view(), name='quill-post-create'),

    ################################################ api

    path('api/', include(router.urls)),
]
