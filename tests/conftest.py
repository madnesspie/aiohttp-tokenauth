import aiohttp_tokenauth
import pytest
from aiohttp import web

pytest_plugins = 'aiohttp.pytest_plugin'


async def user_loader(token: str) -> dict:
    user = None
    if token == 'fake-token':
        user = {'uuid': 'fake-uuid'}
    return user


async def example_resource(request):
    return web.json_response(request.get('user', {}))


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application(middlewares=[
        aiohttp_tokenauth.token_auth_middleware(
            user_loader=user_loader,
            exclude_routes=('/exclude',),
            exclude_methods=('POST',),
        ),
    ])
    app.router.add_route('*', '/', example_resource)
    app.router.add_get('/exclude', example_resource)
    app.router.add_get('/exclude/{user}/orders', example_resource)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def token():
    return 'Bearer fake-token'
