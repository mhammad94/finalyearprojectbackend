from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from graphql import GraphQLError

class UnauthorizedError(GraphQLError):
    def __init__(self, message="You do not have permission to access this resource."):
        super(UnauthorizedError, self).__init__(message, extensions={"status_code": 401})
def login_required_custom(func):
    def wrapper(*args, **kwargs):
        user = args[1].context.user

        if user is None or not user.is_authenticated:
                raise UnauthorizedError("You do not have permission to access this resource.", status_code=401)
        return func(*args, **kwargs)

    return wrapper