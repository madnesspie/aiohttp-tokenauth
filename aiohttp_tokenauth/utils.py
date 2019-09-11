import re


def is_exclude(request, exclude):
    for pattern in exclude:
        if re.match(pattern, request.path):
            return True
    return False
