from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/library/comment/<int:topic_id>/', consumers.CommentConsumer),
]
