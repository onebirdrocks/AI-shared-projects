import pytest
import os
import shutil
from config import get_config

config = get_config()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    # 创建测试用的上传目录和数据库目录
    os.makedirs(config['UPLOAD_DIR'], exist_ok=True)
    os.makedirs(config['DB_PATH'], exist_ok=True)
    
    # 在这里可以添加其他测试环境设置
    
    yield
    
    # 测试结束后清理
    shutil.rmtree(config['UPLOAD_DIR'])
    shutil.rmtree(config['DB_PATH'])