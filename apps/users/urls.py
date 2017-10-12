from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^users/subscribe/(?P<user_id>\d+)/$', views.SubscribeToUser.as_view(), name='user_subscribe'),
    url(r'^users/unsubscribe/(?P<user_id>\d+)/$', views.UnsubscribeFromUser.as_view(), name='user_unsubscribe'),
    
    url(r'^settings/$', views.UserEditView.as_view(), name='user_edit'),
    url(r'profile/$', views.ProfileView.as_view(), name="user_profile"),

    url(r'^posts/create$', views.UserPostCreateView.as_view(), name='user_post_create'),
    url(r'^posts/(?P<pk>\d+)/$', views.UserPostDetail.as_view(), name='user_post_detail'),

    url(r'^news/$', views.UserPostList.as_view(), name='user_post_list'),
    # url(r'^settings/delete-account$', UserDeleteView.as_view(), name='user_settings_delete'),
]