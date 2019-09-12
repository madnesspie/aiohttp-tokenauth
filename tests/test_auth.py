import aiohttp_tokenauth
import pytest
from aiohttp import web


class TestHttpMethods:

    @pytest.mark.parametrize('method', ['GET', 'PUT', 'DELETE'])
    async def test_http_methods(self, cli, method, token):
        resp = await cli.request(method, '/', headers={'Authorization': token})
        assert resp.status == 200
        assert await resp.json() == {'uuid': 'fake-uuid'}

class TestExcluded:

    async def test_method_without_token(self, cli):
        resp = await cli.post('/')
        assert resp.status == 200
        assert await resp.json() == {}

    async def test_path_without_token(self, cli):
        resp = await cli.get('/exclude')
        assert resp.status == 200
        assert await resp.json() == {}

    async def test_regexes_path_without_token(self, cli):
        resp = await cli.get('/exclude/someuser/info')
        assert resp.status == 200
        assert await resp.json() == {}


class TestHttpExceptions:

    @pytest.mark.parametrize(
        'headers, status, message',
        [
            ({}, 401, '401: Missing authorization header'),
            ({
                'Authorization': ''
            }, 403, '403: Invalid authorization header'),
            ({
                'Authorization': 'Bearer'
            }, 403, '403: Invalid authorization header'),
            ({
                'Authorization': 'Invalid-scheme token'
            }, 403, '403: Invalid token scheme'),
            ({
                'Authorization': 'Bearer wrong-token'
            }, 403, '403: Token doesn\'t exist'),
        ],
        ids=[
            'header is missing',
            'token and schema is missing',
            'token is missing',
            'wrong scheme',
            'wrong token',
        ],
    )
    async def test_wrong_header(self, cli, headers, status, message):
        resp = await cli.get('/', headers=headers)
        assert resp.status == status
        assert await resp.text() == message


class TestInstance:

    async def user_loader(self):
        pass

    class UserLoader():

        def __call__(self):
            pass

    @pytest.mark.parametrize(
        'callable_loader',
        [lambda: True, user_loader, UserLoader()],
        ids=['function', 'coroutine', 'callable class'],
    )
    async def test_calables_is_allowed(self, callable_loader):
        try:
            web.Application(middlewares=[
                aiohttp_tokenauth.token_auth_middleware(callable_loader),
            ])
        except TypeError:
            pytest.fail("Unexpected TypeError")

    async def test_uncalables_is_not_allowed(self):
        with pytest.raises(TypeError):
            web.Application(middlewares=[
                aiohttp_tokenauth.token_auth_middleware(user_loader=111)
            ])
