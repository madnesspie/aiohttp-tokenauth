import pytest


async def user_loader(token: str) -> dict:
    user = None
    if token == 'fake-token':
        user = {'uuid': 'fake-uuid'}
    return user
