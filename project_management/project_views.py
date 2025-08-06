from .models import Project
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# GET 
# Return all projects for a user

# POST
# Create a new project for a user

@csrf_exempt
def project_get_post(request):
    if request.method == "GET":
        projects = list(Project.objects.all().values()) # query set to list of dicts
        res = {
            "data": projects
        }
        return JsonResponse(res)

    if request.method == "POST":
        request_data = json.loads((request.body).decode("utf-8"))
        
        print("request_data", request_data)

        # extract name, description, owner
        name = request_data.get("name", "")
        description = request_data.get("description")
        owner = request_data.get("owner")

        # validation
        missing_fields = []
        if not name:
            missing_fields.append("name")
        if not owner:
            missing_fields.append("owner")

        if len(missing_fields) != 0:
            return JsonResponse({
                "missing_fields": missing_fields
            }, status=400)

        try:
            user = User.objects.get(id=owner)
        except User.DoesNotExist:
            return JsonResponse({
                "error": "No such user exists."
            }, status=400) 

        # Create Project Record
        new_project = Project.objects.create(name=name, description=description, owner=user)
        new_project.save()

        return HttpResponse(status=201)


# GET 
# Return specific project by id for a user

# PUT
# Update specific project by id for a user

# DELETE
# Delete specific project by id for a user

@csrf_exempt
def project_get_put_delete(request, project_id):
    if not project_id:
        return JsonResponse({
            "missing_field": "project id"
        }, status=400)

    try:
        project = Project.objects.get(id=project_id)
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