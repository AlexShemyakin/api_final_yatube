from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet, PostViewSet, FollowViewSet, GroupViewSet

router_1 = routers.DefaultRouter()
router_1.register(
    r'follow',
    FollowViewSet,
    basename='following'
)
router_1.register(r'posts', PostViewSet)
router_1.register(r'groups', GroupViewSet)
router_1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
