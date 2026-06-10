from django.http import HttpResponse


class LocalCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        allowed_origins = {
            "http://127.0.0.1:5500",
            "http://localhost:5500",
        }

        if request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = self.get_response(request)

        if origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response["Access-Control-Max-Age"] = "86400"

        return response
