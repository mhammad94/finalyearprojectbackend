def jwt_payload_handler(user, context=None):
    return {
        'user_id': str(user.id),
        'email': user.email,
        "username":user.username
    }