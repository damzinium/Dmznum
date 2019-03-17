from django.apps import AppConfig

class LibraryConfig(AppConfig):
    name = 'library'

    def ready(self):
    	Department = self.get_model("Department")
    	Course = self.get_model("Course")
    	Topic = self.get_model("Topic")
    	