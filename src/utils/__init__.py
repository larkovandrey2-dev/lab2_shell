from .helpers import ensure_exists, move_to_trash, normalize


commands = [ensure_exists, move_to_trash, normalize]
__all__ = [
    "commands",
]
