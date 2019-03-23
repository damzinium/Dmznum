# from django.contrib import admin
# from .models import Institution, School, Course, Topic, Department, Ugrc, Ugrc_Topic, Comment, Reply, CourseSelection

# # Register your models here.
# admin.site.register(School)
# admin.site.register(Institution)
# admin.site.register(Course)
# admin.site.register(Topic)
# admin.site.register(Department)
# admin.site.register(Ugrc)
# admin.site.register(Ugrc_Topic)
# admin.site.register(CourseSelection)

# @admin.register(Reply)
# class ReplyAdmin(admin.ModelAdmin):
#     list_display = ('replier', 'reply', 'date_uploaded',)
#     list_display_links = ('replier',)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     exclude = ('comment', 'commenter',)
#     list_display = ('commenter', 'comment', 'is_approved', 'date_uploaded',)
#     list_editable = ('is_approved',)
#     readonly_fields = ('commenter', 'comment',)
