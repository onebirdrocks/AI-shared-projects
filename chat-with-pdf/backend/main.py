import logging
from fastapi import FastAPI, UploadFile, File, WebSocket, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from services.pdf_service import process_pdf, get_file_list
from services.chat_service import get_chat_response, get_model_info
from config import get_config

import os
from pathlib import Path

config = get_config()

# 确保上传目录存在
os.makedirs(config['UPLOAD_DIR'], exist_ok=True)
os.makedirs(config['DB_PATH'], exist_ok=True)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config['CORS_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置日志
logging.basicConfig(level=config['LOG_LEVEL'])
logger = logging.getLogger(__name__)

logger.info("Application configuration:")
for key, value in config.items():
    logger.info(f"{key}: {value}")

# 添加这行日志
logger.info(f"ALLOW_DANGEROUS_DESERIALIZATION: {config['ALLOW_DANGEROUS_DESERIALIZATION']}")

class ChatQuery(BaseModel):
    query: str
    file_name: str
    chat_history: list

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."},
    )

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只允许上传PDF文件")
        
        content = await file.read()
        if len(content) > config['MAX_UPLOAD_SIZE']:
            raise HTTPException(status_code=400, detail="文件大小超过限制")
        
        file_path = f"{config['UPLOAD_DIR']}/{file.filename}"
        
        # 如果文件已存在，先删除旧文件
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Existing file removed: {file_path}")
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        logger.info(f"Processing PDF: {file_path}")
        
        process_pdf(file_path)
        logger.info(f"PDF上传并处理成功: {file.filename}")
        return {"message": "PDF上传并处理成功", "file_name": file.filename}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"处理PDF时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理PDF时出错: {str(e)}")

@app.get("/files")
async def get_files():
    try:
        files = get_file_list()
        return {"files": files}
    except Exception as e:
        logger.error(f"获取文件列表时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="获取文件列表失败")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            query = data["query"]
            file_name = Path(data["file_name"]).stem  # 移除 .pdf 扩展名
            chat_history = data["chat_history"]
            
            try:
                response = get_chat_response(query, file_name, chat_history)
                await websocket.send_json({"response": response})
            except FileNotFoundError as e:
                logger.error(f"FAISS index file not found: {str(e)}")
                await websocket.send_json({"error": f"无法找到文件索引，请确保文件已正确上传和处理: {file_name}"})
            except Exception as e:
                logger.error(f"Error in chat response: {str(e)}")
                await websocket.send_json({"error": f"生成回答时出错: {str(e)}"})
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket错误: {str(e)}")
        await websocket.send_json({"error": "处您的请求时发生错误"})

@app.get("/model-info")
async def model_info():
    try:
        info = get_model_info()
        return info
    except Exception as e:
        logger.error(f"获取模型信息时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="获取模型信息失败")

@app.get("/pdf/{file_name}")
async def get_pdf(file_name: str):
    file_path = os.path.join(config['UPLOAD_DIR'], file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf')
    else:
        raise HTTPException(status_code=404, detail="PDF file not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config['SERVER_HOST'], port=config['SERVER_PORT'])