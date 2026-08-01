"""
益阳高新区智慧招商平台 — 配置管理
"""
import os


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yiyang-invest-dev-secret-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False


class DevConfig(Config):
    """开发环境配置"""
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "yiyang_invest.db")}'


class ProdConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://yiyang:changeme@localhost:5432/yiyang_invest'
    )


class UploadConfig:
    """文件上传配置"""
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}


def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    return ProdConfig() if env == 'production' else DevConfig()
