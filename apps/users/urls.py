from django.conf.urls import url
from .views import UserDetail, UserList, UserEditView, ProfileView, SubscribeToUser, UnsubscribeFromUser

urlpatterns = [
    url(r'^users/$', UserList.as_view(), name='user_list'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^users/subscribe/(?P<user_id>\d+)/$', SubscribeToUser.as_view(), name='user_subscribe'),
    url(r'^users/unsubscribe/(?P<user_id>\d+)/$', UnsubscribeFromUser.as_view(), name='user_unsubscribe'),
    
    url(r'^settings/$', UserEditView.as_view(), name='user_edit'),
    url(r'profile/$', ProfileView.as_view(), name="user_profile")
    # url(r'^settings/delete-account$', UserDeleteView.as_view(), name='user_settings_delete'),
]