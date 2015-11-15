from django.conf.urls import url
from .views import UserProfileDetailView, UserProfileUpdateView

urlpatterns = [
    url(r'^profile/$', UserProfileDetailView.as_view(), name='user_profile'),
    url(r'^update-user-profile/$',
        UserProfileUpdateView.as_view(),
        name='update_user_profile'),
]
