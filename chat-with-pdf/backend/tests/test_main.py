import pytest
from fastapi.testclient import TestClient
from main import app
from config import get_config
import json

client = TestClient(app)
config = get_config()

def test_upload_pdf():
    with open("tests/test_files/test.pdf", "rb") as f:
        response = client.post("/upload-pdf", files={"file": ("test.pdf", f, "application/pdf")})
    assert response.status_code == 200
    assert "file_name" in response.json()

def test_upload_large_pdf():
    # 创建一个超过最大允许大小的文件
    large_content = b"0" * (config['MAX_UPLOAD_SIZE'] + 1)
    response = client.post("/upload-pdf", files={"file": ("large.pdf", large_content, "application/pdf")})
    assert response.status_code == 400
    assert "文件大小超过限制" in response.json()["error"]

def test_upload_non_pdf():
    with open("tests/test_files/test.txt", "rb") as f:
        response = client.post("/upload-pdf", files={"file": ("test.txt", f, "text/plain")})
    assert response.status_code == 400
    assert "只允许上传PDF文件" in response.json()["error"]

def test_get_files_empty():
    # 确保文件列表为空
    import os
    for file in os.listdir(config['UPLOAD_DIR']):
        os.remove(os.path.join(config['UPLOAD_DIR'], file))
    
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json()["files"] == []

def test_get_files_with_content():
    # 上传一个文件
    with open("tests/test_files/test.pdf", "rb") as f:
        client.post("/upload-pdf", files={"file": ("test.pdf", f, "application/pdf")})
    
    response = client.get("/files")
    assert response.status_code == 200
    assert "test.pdf" in response.json()["files"]

def test_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200
    assert "llm" in response.json()
    assert "embeddings" in response.json()

@pytest.mark.asyncio
async def test_websocket_valid_query():
    with client.websocket_connect("/ws") as websocket:
        data = {"query": "Test query", "file_name": "test.pdf", "chat_history": []}
        await websocket.send_json(data)
        response = await websocket.receive_json()
        assert "response" in response

@pytest.mark.asyncio
async def test_websocket_invalid_json():
    with client.websocket_connect("/ws") as websocket:
        await websocket.send_text("Invalid JSON")
        response = await websocket.receive_json()
        assert "error" in response

@pytest.mark.asyncio
async def test_websocket_missing_fields():
    with client.websocket_connect("/ws") as websocket:
        data = {"query": "Test query"}  # Missing file_name and chat_history
        await websocket.send_json(data)
        response = await websocket.receive_json()
        assert "error" in response

def test_error_handling():
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404
    assert "error" in response.json()

# 模拟服务异常
def test_internal_server_error(monkeypatch):
    def mock_get_files():
        raise Exception("Simulated internal error")
    
    monkeypatch.setattr("services.pdf_service.get_file_list", mock_get_files)
    response = client.get("/files")
    assert response.status_code == 500
    assert "error" in response.json()