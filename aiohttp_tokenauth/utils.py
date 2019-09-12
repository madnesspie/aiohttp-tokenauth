import re


def is_exclude(request, exclude):
    for pattern in exclude:
        if re.fullmatch(pattern, request.path):
            return True
    return False
