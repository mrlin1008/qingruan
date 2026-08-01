"""
益阳高新区智慧招商平台 — Gunicorn WSGI 入口
"""
from app import app
from werkzeug.middleware.proxy_fix import ProxyFix

# 信任 Nginx 转发的 X-Forwarded-Proto / X-Forwarded-For
# 确保 Flask 在 HTTPS 反向代理后生成正确的 url_for / redirect
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

if __name__ == '__main__':
    app.run()
