from functools import wraps
from flask import url_for, redirect, abort
from flask_login import current_user


def roles_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('users.login'))
            if not current_user.allowed(roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
