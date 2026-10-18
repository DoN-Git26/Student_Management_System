"""Decorators for logging, authentication, authorisation and validation."""

import functools
import logging

from utils import auth

logger = logging.getLogger("attendance")


def log_action(func):
    """Log each call and any error it raises."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("running %s", func.__name__)
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.error("%s failed: %s", func.__name__, exc)
            raise
    return wrapper


def login_required(func):
    """Require a logged-in user and pass it to the command as 'user'."""
    @functools.wraps(func)
    def wrapper(args):
        user = auth.current_user()
        if user is None:
            raise auth.AuthError("Please log in first (use the 'login' command).")
        return func(args, user)
    return wrapper


def role_required(*roles):
    """Allow only the listed roles to run the command."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args, user):
            if user.role not in roles:
                raise auth.AuthError(
                    f"Access denied: this action needs the role {' or '.join(roles)}."
                )
            return func(args, user)
        return wrapper
    return decorator


def require_args(*names):
    """Reject the command if a named argument is missing or blank."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args, *rest):
            for name in names:
                value = getattr(args, name, None)
                if value is None or not str(value).strip():
                    raise ValueError(f"'{name}' is required.")
            return func(args, *rest)
        return wrapper
    return decorator
