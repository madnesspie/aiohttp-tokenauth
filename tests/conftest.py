import pytest
from aiohttp import web

import aiohttp_tokenauth

pytest_plugins = 'aiohttp.pytest_plugin'


async def user_loader(token: str) -> dict:
    user = None
    if token == 'fake-token':
        user = {'uuid': 'fake-uuid'}
    return user


async def example_resource(request):
    return web.json_response(request['user'])


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application(middlewares=[
        aiohttp_tokenauth.token_auth_middleware(user_loader),
    ])
    app.router.add_route('*', '/', example_resource)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def token():
    return 'Bearer fake-token'
