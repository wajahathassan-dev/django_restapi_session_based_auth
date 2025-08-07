from .models import Project
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# GET 
# Return all projects for a user

# POST
# Create a new project for a user

@csrf_exempt
@login_required
def project_get_post(request):
    try:
        logged_in_user = request.user
        if request.method == "GET":
            projects = list(Project.objects.filter(owner=logged_in_user).values()) # query set to list of dicts
            res = {
                "data": projects
            }
            return JsonResponse(res)

        if request.method == "POST":
            request_data = json.loads((request.body).decode("utf-8"))

            # extract name, description, owner
            name = request_data.get("name", "")
            description = request_data.get("description")

            # validation
            missing_fields = []
            if not name:
                missing_fields.append("name")

            if len(missing_fields) != 0:
                return JsonResponse({
                    "missing_fields": missing_fields
                }, status=400)

            # Create Project Record
            new_project = Project.objects.create(name=name, description=description, owner=logged_in_user)
            new_project.save()

            return HttpResponse(status=201)

        return HttpResponse(status=404)
    except Exception as e:
        return JsonResponse({
            "msg": str(e)
        }, status=500)

# GET 
# Return specific project by id for a user

# PUT
# Update specific project by id for a user

# DELETE
# Delete specific project by id for a user

@csrf_exempt
@login_required
def project_get_put_delete(request, project_id):
    try:
        logged_in_user = request.user
        try:
            project = Project.objects.get(id=project_id, owner=logged_in_user)
        except Project.DoesNotExist:
            return JsonResponse({
                "msg": "No such project exists"
            }, status=400)
        
        if request.method == "GET":
            return JsonResponse({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at
            })

        if request.method == "PUT":
            request_data = (request.body).decode("utf-8")
            request_data = json.loads(request_data)
            
            name = request_data.get("name")
            description = request_data.get("description")
            
            # validation
            missing_fields = []

            if name is None:
                missing_fields.append("name")
            if description is None:
                missing_fields.append("description")
            
            if len(missing_fields) > 0:
                return JsonResponse({
                    "missing_fields": missing_fields
                }, status=400)
            
            # update project
            project.name = name
            project.description = description

            project.save()

            return JsonResponse({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at
            })

        if request.method == "DELETE":
            project.delete()
            return HttpResponse()
        
        return HttpResponse(status=404)
    except Exception as e:
        return JsonResponse({
            "msg": str(e)
        }, status=500)