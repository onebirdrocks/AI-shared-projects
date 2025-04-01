1. 程序的后端，用于构建后端API服务，提供高性能的异步处理能力。 
- 编程语言：Python 版本3.10
- Rest API使用：FastAPI。上传PDF的API路径 (/upload-pdf)。用户查询对话的API路径 (/query-chat)。
- 跨域支持：使用FastAPI的CORS中间件，允许前端与后端进行跨域通信。
- RAG应用使用Langchain
- 大语言模型通过ollma运行在本地电脑上，使用qwen2的模型。
- 上传pdf的时候，按照传统rag的流程切分成小的chunks后，进行embedding后，写入向量数据库。关于PDF的分块和向量化处理，分块的大小可以让每个chunk的字符数（如50-100字符），可以使用Langchain的具体方法：CharacterTextSplitter。pdf上传后保存在pdf目录下
- 用户聊天时的提问内容，也需要进行 embedding后发送到向量数据库进行查询
- embedding使用运行在ollama上的 nomic-embed-text模型
- 向量数据库使用FAISS。FAISS的索引方法和检索使用IndexFlatL2 。FAISS的索引存放在db目录中。
- 支持用户和AI的多轮对话，对话历史信息要作为上下文保留在prompt中。
- 配置管理：将关键配置如数据库路径、模型路径等集中在config.py文件中，并支持通过环境变量进行配置。


2. 前端部分
- 编程语言：Node 版本v20.17，前端代码使用Typescript编写
- 前端框架使用React
- CSS框架使用Tailwind
- 前端实时聊天功能：通过WebSocket或SSE（Server-Sent Events）实现前端与后端的双向通信，确保聊天消息的及时响应。当页面的websocket断了，需要有相关的提示信息，需要能够重新连接，成功后将出错信息消除。

3. 依赖管理
- 所有后端的依赖项应写入requirements.txt文件。并且确保这些依赖的版本和python的版本都要兼容
- 一些已知的python依赖 
langchain==0.2.16
langchain-community==0.2.16
langchain-core==0.2.38
langchain-text-splitters==0.2.4
fastapi==0.109.2
faiss-cpu==1.7.3
ollama==0.3.2
langchain-ollama==0.1.3
uvicorn==0.24.0
python-multipart==0.0.6
pypdf==3.17.1
pydantic==2.5.2
python-dotenv==1.0.0
websockets==10.4

- 所有的node相关的依赖，放在package.json中。请使用下面的一些已知的库和版本。
"axios": "^0.24.0",
"react": "^18.2.0",
"react-dom": "^18.2.0",
"react-dropzone": "^11.4.2",
"react-router-dom": "^6.0.0",
"react-scripts": "^5.0.1",
"tailwindcss": "^2.2.19",
"http-proxy-middleware": "^2.0.1"


4. 编码规范
- 遵循langchain，react等业界规范
- 在项目跟目录下生成.gitignore 文件：确保排除 node_modules/、build/、dist/、__pycache__/、env/ 等目录，以避免提交不必要的依赖和编译文件。

前端代码：
在项目根目录下创建frontend目录，存放相关前端代码。目录结构示例：
/frontend/            # 前端代码目录
│   ├── /assets          # 静态资源（图片、字体、样式等）
│   ├── /components      # React 组件目录
│   ├── /hooks           # 自定义 React hooks
│   ├── /pages           # 页面级别组件
│   ├── /context         # React Context
│   ├── /types           # 类型定义
│   ├── /styles          # 全局样式文件
│   ├── /public          # 前端公共资源文件夹
│   │   └── index.html   # React 应用的模板文件
│   ├── App.tsx          # 主应用入口组件
│   ├── index.tsx        # React 应用入口文件
│   ├── react-app-env.d.ts  # TypeScript 环境配置文件
│   └── package.json     # 前端依赖和脚本配置文件


后端代码：
在项目根目录下创建backend目录，目录结构示例：
/backend/
├── db/                 # FAISS数据文件存放目录
├── models/             # 数据模型与嵌入逻辑
├── routes/             # API 路由
├── services/           # 各种服务逻辑（如FAISS操作、模型调用等）
└── main.py             # 主应用入口
config.py：集中管理配置项，如数据库路径、模型路径等。


5. 日志
- 日志级别：设置为INFO级别。
- 日志输出：在合适的部分增加必要的输出到控制台，方便理解和调试代码，并且可以根据需要进一步配置输出到日志文件。
- 日志内容：所有关键流程，例如pdf上传、向量生成、查询请求、prompt内容的生成，模型响应等信息的记录。

6. 文档

- README：包含程序的简介、使用方法、安装步骤、运行命令、以及相关示例。项目介绍：简要介绍项目的功能和目标。使用说明：包括如何上传pdf文件、如何进行聊天。安装步骤：详细描述如何安装依赖项、配置环境、运行后端和前端服务。目录结构：清晰列出前后端目录结构，帮助开发者快速理解代码组织方式。Readme文件生成两份 readme.md放英文版，readme-cn.md放中文版
- 在跟目录下创建docs目录，相关API的交互以及架构发生变化，请记得更新这两个文档
/docs
├── api-docs.md        # API 交互文档
└── architecture.md    # 项目架构文档
