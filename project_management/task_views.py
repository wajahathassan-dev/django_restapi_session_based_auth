from .models import Project, Task
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# GET
# Get all tasks for a project

# POST
# Create a new task in a project
@csrf_exempt
@login_required
def task_get_put_by_project(request, project_id):
    try:
        logged_in_user = request.user
        try:
            project = Project.objects.get(id=project_id, owner=logged_in_user)
        except Project.DoesNotExist:
            return JsonResponse({
                "msg": "No such project exists"
            }, status=400)

        if request.method == "GET":
            tasks = list(Task.objects.filter(project=project).values())
            return JsonResponse({
                "data": tasks
            })
        
        if request.method == "POST":
            request_data = json.loads(request.body)

            # validation

            data = request_data.get("data")
            if data is None:
                return JsonResponse({"missing_fields": ["data"]}, status=400)
            
            tasks = []
            for item in data:
                title = item.get("title", "").strip()
                description = item.get("description")
                is_completed = item.get("is_completed", False)
                due_date = item.get("due_date")

                missing_fields = []
                if not title:
                    missing_fields.append("title")
                if due_date is None:
                    missing_fields.append("due_date")

                if len(missing_fields) > 0:
                    return JsonResponse({
                        "missing_fields": missing_fields
                    }, status=400)

                tasks.append(Task(
                                project=project,
                                title=title,
                                description=description,
                                is_completed=is_completed,
                                due_date=due_date))
            
            Task.objects.bulk_create(tasks)
            return HttpResponse(status=201)
        
        return HttpResponse(status=404)
    except Exception as e:
        return JsonResponse({
            "msg": str(e)
        }, status=500)


# PUT
# Update a task

# DELETE
# Delete a task
@csrf_exempt
@login_required
def task_put_delete(request, task_id):
    try:
        logged_in_user = request.user
        try:
            task = Task.objects.get(id=task_id, project__owner = logged_in_user)            
        except Task.DoesNotExist:
            return JsonResponse({
                "msg": "No such task exists"
            }, status=400)

        if request.method == "GET":
            return JsonResponse({
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "due_date": task.due_date,
                "created_at": task.created_at
            })

        if request.method == "PUT":
            request_data = json.loads(request.body)

            # validation
            title = request_data.get("title", "").strip()
            description = request_data.get("description")
            is_completed = request_data.get("is_completed")
            due_date = request_data.get("due_date")

            missing_fields = []
            if not title:
                missing_fields.append("title")
            if is_completed is None:
                missing_fields.append("is_completed")
            if not due_date:
                missing_fields.append("due_date")
            
            if len(missing_fields) > 0:
                return JsonResponse({
                    "missing_fields": missing_fields
                }, status=400)

            # update
            task.title = title
            task.description = description
            task.is_completed = is_completed
            task.due_date = due_date
            task.save()

            return JsonResponse({
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "due_date": task.due_date,
                "created_at": task.created_at
            }, status=200)

        if request.method == "DELETE":
            task.delete()
            return HttpResponse()
        
        return HttpResponse(status=404)
    except Exception as e:
        return JsonResponse({
            "msg": str(e)
        }, status=500)
