from functools import wraps

from flask import abort, redirect, url_for
from flask_login import current_user
from sqlalchemy import func


def roles_required(roles):
    """Checks if Current User has at least one of acceptable roles and redirects him accordingly

    :param roles: List of Acceptable roles
    :return: 403 page if User os not allowed and Login page if User is not Authenticated
    """
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


def get_count(q):
    """Count number of results in SQLAlchemy statement

    :param q: SQLAlchemy Query
    :return: Number of Results (Integer)
    """
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count
