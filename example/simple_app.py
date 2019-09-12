from aiohttp import web
from aiohttp_tokenauth import token_auth_middleware


async def example_resource(request):
    return web.json_response(request['user'])


async def init():

    async def user_loader(token: str):
        """Checks that token is valid

        It's the callback that will get the token from "Authorization" header.
        It can check that token is exist in a database or some another place.

        Args:
            token (str): A token from "Authorization" http header.

        Returns:
            Dict or something else. If the callback returns None then
            the aiohttp.web.HTTPForbidden will be raised.
        """
        user = None
        if token == 'fake-token':
            user = {'uuid': 'fake-uuid'}
        return user

    app = web.Application(middlewares=[token_auth_middleware(user_loader)])
    app.router.add_get('/', example_resource)
    return app


if __name__ == '__main__':
    web.run_app(init())
