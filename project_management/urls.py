from django.urls import path
from .project_views import project_get_post, project_get_put_delete
from .task_views import task_get_put_by_project, task_put_delete
from .auth_views import login_view, logout_view

urlpatterns = [
    path("login/", login_view),
    path("logout/", logout_view),
    path("project/", project_get_post),
    path("project/<int:project_id>/", project_get_put_delete),
    path("project/task/<int:project_id>/", task_get_put_by_project),
    path("task/<int:task_id>/", task_put_delete),
]