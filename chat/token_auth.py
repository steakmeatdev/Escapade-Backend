from django.contrib.auth.models import AnonymousUser

# We can get things from db while waiting to things to finish
from channels.db import database_sync_to_async

# Changing the middleware
from channels.middleware import BaseMiddleware

# Getting the access token
from rest_framework_simplejwt.tokens import AccessToken
from useraccount.models import User


# Get the user if he's authenticated
@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token.payload["user_id"]
        return User.objects.get(pk=user_id)
    except Exception as e:
        return AnonymousUser


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Split the URL
        query = dict((x.split("=") for x in scope["query_string"].decode().split("&")))
        token_key = query.get("token")
        # Scope is like thes session, append user to it
        scope["user"] = await get_user(token_key)
        return await super().__call__(scope, receive, send)
