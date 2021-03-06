# from django.contrib import admin

# from .models import Profile, User
# from .forms import ProfileForm

# admin.site.site_title = 'Damzinium Administration'
# admin.site.site_header = 'Damzinium Administration'


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'


# class CustomUserAdmin(admin.ModelAdmin):
#     # form = ProfileForm
#     # inlines = (ProfileInline,)
#     exclude = ('profile',)
#     readonly_fields = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'password', 'last_login', 'date_joined')
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
#     list_editable = ('is_active',)
#     search_fields = ('username', 'first_name', 'last_name', 'email')

#     # def phone_number(self, instance):
#     #     return instance.profile.phone_number

#     # phone_number.short_description = ('phone')

#     # def department_name(self, instance):
#     #     return instance.profile.department_name

#     # department_name.short_description = ('department')

#     # def get_inline_instances(self, request, obj=None):
#     #     if not obj:
#     #         return list()
#     #     return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth import get_user_model

admin.site.register(get_user_model())