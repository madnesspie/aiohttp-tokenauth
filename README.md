# aiohttp-tokenauth

Aiohttp simple token auth middleware that can check any token that assign to user or group of users in database or some another place.

## Installation
```bash
pip install aiohttp_tokenauth
```

## Documentation

### Basic usage
First of all, let's create a simple app.
```python
# Full text in example/simple_app.py
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
```
Then, run the aiohttp app.
```bash
$ python example/simple_app.py
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```
Now try to get access to url with token in "Authorization" header.
```bash
$ curl -H 'Authorization: Bearer fake-token' http://0.0.0.0:8080
{"uuid": "fake-uuid"}
```
And result without token.
```bash
$ curl http://0.0.0.0:8080
401: Missing authorization header
```

### Ignoring routes and http methods
You can ignore specific routes, app the paths to "exclude_routes".
```python
app = web.Application(middlewares=[
    token_auth_middleware(
        user_loader=user_loader,
        # You can use regular expressions here
        exclude_routes=('/exclude', r'/exclude/\w+/info'),
        exclude_methods=('POST',),
    ),
])
```

### Change auth scheme
For changing the scheme (prefix in "Authorization" header) use `auth_scheme` argument.
```python
app = web.Application(middlewares=[
    token_auth_middleware(
        user_loader=user_loader,
        auth_scheme='Token',
    ),
])
```
Now such request is valid:
```bash
$ curl -H 'Authorization: Token fake-token' http://0.0.0.0:8080
{"uuid": "fake-uuid"}
```
