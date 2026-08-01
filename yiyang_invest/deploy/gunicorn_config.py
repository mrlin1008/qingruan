# Gunicorn 配置文件
bind = "127.0.0.1:8000"
workers = 2
worker_class = "sync"
timeout = 120
accesslog = "/var/log/yiyang_invest/gunicorn_access.log"
errorlog = "/var/log/yiyang_invest/gunicorn_error.log"
loglevel = "info"
