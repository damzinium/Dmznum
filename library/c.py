import json

from asgiref.sync import async_to_sync # converts async functions to sync functions
from channels.generic.websocket import WebsocketConsumer

from .models import Comment, Topic


class CommentConsumer(WebsocketConsumer):
    def connect(self):
        """
        handles a connection to this websocket
        """
        # get the topic id from the url
        self.topic_id = self.scope['url_route']['kwargs']['topic_id']
        try:
            # accept connection and add user to the topic group if the topic exists
            Topic.objects.get(id=self.topic_id)
            self.topic_group_name = 'topic_{}'.format(self.topic_id)
            async_to_sync(self.channel_layer.group_add)(
                self.topic_group_name,
                self.channel_name
            )
            self.accept()
        except Topic.DoesNotExist:
            # if the topic doesn't exist, close the connection
            self.close(code=404)
    
    def disconnect(self, close_code):
        """
        handles disconnection from this websocket
        """
        # remove the user from the topic group
        async_to_sync(self.channel_layer.group_discard)(
            self.topic_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        """
        handles new comments comming in
        """
        # generate a python dict from the json data parsed
        text_data_json = json.loads(text_data)
        # get the topic id
        topic_id = text_data_json['topic_id']
        # get the comment
        comment = text_data_json['comment']
        # get the topic matching the topic id
        topic = Topic.objects.get(id=topic_id)
        # create a new comment with the topic, comment and user
        new_comment = Comment.objects.create(
            topic=topic,
            comment=comment,
            commenter=self.scope['user'] # self.scope contains data in the session
        )
        # send the comment to the topic group
        async_to_sync(self.channel_layer.group_send)(
            self.topic_group_name,
            {
                'type': 'topic_comment',
                'username': str(new_comment.commenter.username),
                'profile_picture': str(new_comment.commenter.profile.profile_picture),
                'comment': str(new_comment.comment),
                'date_uploaded': str(new_comment.date_uploaded),
            }
        )

    def topic_comment(self, event):
        """
        receives comment from the group and sends to users
        """
        self.send(text_data=json.dumps(
            {
                'username': event['username'],
                'profile_picture': event['profile_picture'],
                'comment': event['comment'],
                'date_uploaded': event['date_uploaded'],
            }
        ))