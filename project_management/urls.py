from django.urls import path
from .project_views import project_get_post, project_get_put_delete

urlpatterns = [
    path("project/", project_get_post),
    path("project/<int:project_id>/", project_get_put_delete)
]