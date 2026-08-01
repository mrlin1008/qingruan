"""
益阳高新区智慧招商平台 — 认证与权限
"""
from functools import wraps
from flask import session, redirect, url_for, flash
from models import User


def login_required(f):
    """登录校验装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """角色权限装饰器：admin / manager / staff"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') not in roles:
                flash('权限不足', 'error')
                return redirect(url_for('admin_dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator


def get_current_user():
    """获取当前登录用户对象"""
    uid = session.get('user_id')
    if uid:
        return User.query.get(uid)
    return None
