import json
from django.http import JsonResponse
from graphql import GraphQLError
from graphql_jwt.shortcuts import get_user_by_token

class UnauthorizedError(GraphQLError):
    def __init__(self, message="You do not have permission to access this resource."):
        super(UnauthorizedError, self).__init__(message)


class UnauthorizedMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        token = request.headers.get("Authorization", "")
        host = request.META.get("HTTP_HOST", "")

        # if host == "localhost:8000":
        #     return self.get_response(request)

        if token.startswith("JWT "):
            token = token.split("JWT ")[1]
            user_from_token = get_user_by_token(token)

            if user_from_token is not None:
                user = user_from_token

        if "application/json" in request.headers.get("Content-Type", ""):
            try:
                json_data = json.loads(request.body.decode("utf-8"))
                operation_type = json_data.get("operationName")

                if operation_type == "Logout" or operation_type == "Login":
                    return self.get_response(request)
            except json.JSONDecodeError:
                pass

        if user is None or not user.is_authenticated:
            response_data = {"errors": [str(UnauthorizedError())]}
            response = JsonResponse(response_data, status=401)
            return response
        return self.get_response(request)
