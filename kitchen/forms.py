from django import forms
from django.core.exceptions import ValidationError

from library.models import Course, SubTopic, Topic


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'name',
            'code',
        )


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = (
            'course',
            'title',
            'prev',
        )
        widgets = {
            'course': forms.HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['prev'] is None:
            try:
                Topic.objects.get(course=cleaned_data['course'], prev__isnull=True)
                raise ValidationError({'prev': 'A first topic already exists'})
            except Topic.DoesNotExist:
                pass


class AddSubTopicForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = (
            'topic',
            'title',
            'prev',
        )
        widgets = {
            'topic': forms.HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['prev'] is None:
            try:
                SubTopic.objects.get(topic=cleaned_data['topic'], prev__isnull=True)
                raise ValidationError({'prev': 'A first sub-topic already exists'})
            except SubTopic.DoesNotExist:
                pass


class EditSubTopicInfoForm(AddSubTopicForm):
    class Meta:
        model = SubTopic
        fields = (
            'title',
        )


class EditSubTopicContentForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = (
            'temp_content',
        )
