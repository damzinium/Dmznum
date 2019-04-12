from django.urls import path
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from . import views

app_name = 'kitchen'

urlpatterns = [
# path('', permission_required('perm')(views.PostCreate.as_view()), name='add'),
path('', user_passes_test(lambda u:u.is_staff)(login_required(views.ShowKitchen)), name='index'),
path('course/', user_passes_test(lambda u:u.is_staff)(login_required(views.PostCreate.as_view())), name='add'),
# path('ugrc/', user_passes_test(lambda u:u.is_staff)(login_required(views.UgrcPostCreate.as_view())), name='ugrc_add'),
]