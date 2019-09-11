from typing import Callable, Coroutine, Tuple

from aiohttp import web

from aiohttp_tokenauth import utils


def token_auth_middleware(user_loader: Callable,
                          request_property: str = 'user',
                          auth_scheme: str = 'Bearer',
                          exclude_routes: Tuple = tuple(),
                          exclude_methods: Tuple = tuple()) -> Coroutine:
    """Checks a auth token and adds a user from user_loader in request.

    Aiohttp token auth middleware, that checks the "Authorization" http header
    for token and, if it valid, runs the "user_loader" callback. If user loader
    returns a user, then middleware adds the user to request with key that
    contain the "request_property" variable, else it will raise an HTTPForbidden
    exception.

    Args:
        user_loader (Callable): User loader callback. Must return a user or
            None if user doesn't found by token.
        request_property (str, optional): Key for save in request object.
            Defaults to 'user'.
        auth_scheme (str, optional): Prefix for value in "Authorization" header.
            Defaults to 'Bearer'.
        exclude_routes: (Tuple, optional): Tuple of pathes that will be excluded.
            Defaults to empty tuple.
        exclude_methods(Tuple, optional): Tuple of http methods that will be
            excluded. Defaults to empty tuple.

    Raises:
        TypeError: If user_loader isn't callable object.
        web.HTTPUnauthorized: If "Authorization" token is missing.
        web.HTTPForbidden: Wrong token, schema or header.

    Returns:
        Coroutine: Aiohttp middleware.
    """
    if not callable(user_loader):
        raise TypeError('Must be callable')

    @web.middleware
    async def middleware(request, handler):
        if (utils.is_exclude(request, exclude_routes) or
                request.method in exclude_methods):
            return await handler(request)

        try:
            scheme, token = request.headers['Authorization'].strip().split(' ')
        except KeyError:
            raise web.HTTPUnauthorized(reason='Missing authorization header',)
        except ValueError:
            raise web.HTTPForbidden(reason='Invalid authorization header',)

        if auth_scheme.lower() != scheme.lower():
            raise web.HTTPForbidden(reason='Invalid token scheme',)

        user = await user_loader(token)
        if user:
            request[request_property] = user
        else:
            raise web.HTTPForbidden(reason='Token doesn\'t exist')

        return await handler(request)

    return middleware
