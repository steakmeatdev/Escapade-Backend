from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from useraccount.models import User


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

        # Initialize the MiddleWare
        self.inner = inner

    async def __call__(self, scope, receive, send):

        query_string = scope["query_string"].decode() # Byte string : "b'token=abc&user_id=32'"

     
        pairs = query_string.split("&")  

  
        split_pairs = [pair.split("=") for pair in pairs] 

        
        query = dict(split_pairs)

        token_key = query.get("token")

        scope["user"] = await get_user(token_key)

        return await super().__call__(scope, receive, send)
