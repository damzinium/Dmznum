from django.urls import path
from django.contrib.auth.decorators import permission_required, login_required
from . import views

app_name = 'kitchen'

urlpatterns = [
# path('', permission_required('perm')(views.PostCreate.as_view()), name='add'),
path('', login_required(views.ShowKitchen), name='index'),
path('course/', login_required(views.PostCreate.as_view()), name='add'),
path('ugrc/', login_required(views.UgrcPostCreate.as_view()), name='ugrc_add'),
]