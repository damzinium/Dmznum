from django.core.management.base import BaseCommand

from library.models import Course, Topic, Ugrc


class Command(BaseCommand):
    help = 'merges ugrc model with courses model'

    def handle(self, *args, **kwargs):
        ugrcs = Ugrc.objects.all()
        for ugrc in ugrcs:
            new_course = Course()
            new_course.is_required = True
            new_course.name = ugrc.ugrc
            new_course.code = ugrc.ugrc_code
            new_course.save()

            for topic in ugrc.ugrc_topic_set.all():
                new_topic = Topic()
                new_topic.course = new_course
                new_topic.title = topic.title
                new_topic.content = topic.content
                new_topic.push_updates = True
                new_topic.save()
