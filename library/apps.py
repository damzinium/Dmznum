from django.apps import AppConfig
from watson import search as watson


class LibraryConfig(AppConfig):
    name = 'library'

    def ready(self):
    	Department = self.get_model("Department")
    	Course = self.get_model("Course")
    	Topic = self.get_model("Topic")
    	watson.register(Department)
    	watson.register(Course)
    	watson.register(Topic)
