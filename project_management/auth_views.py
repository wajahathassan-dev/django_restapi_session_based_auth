from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    try:
        if request.method == "POST":
            request_data = json.loads(request.body)

            username = request_data.get("username")
            password = request_data.get("password")

            missing_fields = []
            if username is None:
                missing_fields.append("username")
            if password is None:
                missing_fields.append("password")

            if len(missing_fields) > 0:
                return JsonResponse({
                    "missing_fields": missing_fields
                }, status=400)

            user = authenticate(request, username=username, password=password)

            if not user:
                return JsonResponse({"msg": "Invalid credentials"}, status=401)

            login(request, user=user) # create session
            return JsonResponse({"msg": "login success"})

        return HttpResponse(status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"msg": str(e)}, status=500)
    
@csrf_exempt
def logout_view(request):
    try:
        if request.method == "POST":
            logout(request) # clear session
            return JsonResponse({'msg': 'Logged out successfully'})
        
    except Exception as e:
        return JsonResponse({}, status=500)
