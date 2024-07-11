__VERSION__ = (0, 1, 6)


def get_version() -> str:
    return ".".join(map(str, __VERSION__))
