from fastapi import Request
from fastapi.responses import JSONResponse


class RateLimiterMiddleware:
    def __init__(self, app, redis_client):
        self.app = app
        self.redis_client = redis_client
        self.rate_limit = 30
        self.window = 60

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        ip = request.client.host

        redis_key = f"rate_limit:{ip}"

        count = await self.redis_client.incr(redis_key)

        if count == 1:
            await self.redis_client.expire(redis_key, self.window)

        if count > self.rate_limit:
            response = JSONResponse(
                status_code=429,
                content={"detail": "Too many requests, please try again later."},
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)