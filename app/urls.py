from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('register/', register_request, name='register'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('', models_page, name='models'),
    path('delete_model/<str:model_name>/', delete_model, name='delete_model'),
    path('<str:model_name>/projects', projects_page, name='projects'),
    path('<str:model_name>/delete_project/<str:data_name>/', delete_project, name='delete_project'),
    path('<str:model_name>/<str:data_name>/runs/', runs_page, name='runs'),
    path('<str:model_name>/<str:data_name>/<int:run_id>/', run_details_page, name='run_details'),
    path('<str:model_name>/<str:data_name>/<int:run_id>/delete_run/', delete_run, name='delete_run'),
]
