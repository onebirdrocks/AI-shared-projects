# PDF对话系统

PDF对话系统是一个Web应用程序,允许用户上传PDF文件并通过聊天界面与其内容进行交互。该应用程序使用RAG(检索增强生成)技术,基于上传的PDF内容提供准确的响应。

## 功能特性

- PDF文件上传和管理
- 实时聊天界面
- PDF内容查看
- 基于RAG的问答系统
- 使用WebSocket进行实时通信

## 技术栈

- 前端: React, TypeScript, Tailwind CSS
- 后端: Python, FastAPI
- 机器学习: Langchain, Ollama (qwen2模型), FAISS

## 前置要求

- Node.js v20.17或更高版本
- Python 3.10或更高版本
- 安装了qwen2和nomic-embed-text模型的Ollama

## 安装

### 后端

1. 进入后端目录:
   ```
   cd backend
   ```

2. 创建虚拟环境:
   ```
   python -m venv venv
   ```

3. 激活虚拟环境:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS和Linux:
     ```
     source venv/bin/activate
     ```

4. 安装所需包:
   ```
   pip install -r requirements.txt
   ```

### 前端

1. 进入前端目录:
   ```
   cd frontend
   ```

2. 安装所需包:
   ```
   npm install
   ```

## 配置

1. 在后端目录创建`.env`文件,内容如下:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   UPLOAD_DIR=uploads
   DB_PATH=db
   ```

2. 确保Ollama正在运行,并且已安装所需的模型。

## 运行应用

1. 启动后端服务器:
   ```
   cd backend
   uvicorn main:app --reload
   ```

2. 启动前端开发服务器:
   ```
   cd frontend
   npm start
   ```

3. 打开浏览器,访问`http://localhost:3000`

## 使用方法

1. 使用上传界面上传PDF文件。
2. 从文件列表中选择上传的文件。
3. 在查看器中查看PDF内容。
4. 在聊天界面中询问有关PDF内容的问题。

## API文档

详细的API文档,请参阅`docs/api-docs.md`。

## 架构

有关应用程序架构的信息,请参阅`docs/architecture.md`。

## 贡献

欢迎贡献!请随时提交Pull Request。

## 许可证

本项目采用MIT许可证。