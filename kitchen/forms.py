from django import forms

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
            'title',
            'prev',
        )


class AddSubTopicForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = (
            'title',
            'prev',
        )


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
