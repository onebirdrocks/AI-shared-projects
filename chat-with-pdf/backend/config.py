import os
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载 .env 文件
load_dotenv()

# 服务器配置
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))

# 文件上传配置
UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 10 * 1024 * 1024))  # 默认10MB

# 数据库配置
DB_PATH = os.getenv('DB_PATH', 'db')

# Ollama 配置
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_LLM_MODEL = os.getenv('OLLAMA_LLM_MODEL', 'qwen2')
OLLAMA_EMBED_MODEL = os.getenv('OLLAMA_EMBED_MODEL', 'nomic-embed-text')

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# CORS 配置
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

# 安全配置
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

# 允许危险的反序列化 - 直接在配置文件中设置
ALLOW_DANGEROUS_DESERIALIZATION = True
logger.info(f"ALLOW_DANGEROUS_DESERIALIZATION in config: {ALLOW_DANGEROUS_DESERIALIZATION}")

def get_config():
    return {
        'SERVER_HOST': SERVER_HOST,
        'SERVER_PORT': SERVER_PORT,
        'UPLOAD_DIR': UPLOAD_DIR,
        'MAX_UPLOAD_SIZE': MAX_UPLOAD_SIZE,
        'DB_PATH': DB_PATH,
        'OLLAMA_BASE_URL': OLLAMA_BASE_URL,
        'OLLAMA_LLM_MODEL': OLLAMA_LLM_MODEL,
        'OLLAMA_EMBED_MODEL': OLLAMA_EMBED_MODEL,
        'LOG_LEVEL': LOG_LEVEL,
        'CORS_ORIGINS': CORS_ORIGINS,
        'SECRET_KEY': SECRET_KEY,
        'ALLOW_DANGEROUS_DESERIALIZATION': ALLOW_DANGEROUS_DESERIALIZATION,
    }