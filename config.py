import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True
    
class Config:
    # 搜索配置
    SEARCH_TIMEOUT = 5  # 搜索超时时间（秒）
    MAX_SEARCH_THREADS = 8  # 最大搜索线程数
    
    # 安全配置
    '''
    ALLOWED_EXECUTABLES_FILE = 'allowed_executables.txt''
    '''