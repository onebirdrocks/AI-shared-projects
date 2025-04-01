import logging
import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from config import DB_PATH, OLLAMA_BASE_URL, UPLOAD_DIR, ALLOW_DANGEROUS_DESERIALIZATION

# 在文件开头添加以下代码
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DB_PATH, exist_ok=True)

logger = logging.getLogger(__name__)

# 添加这行日志
logger.info(f"ALLOW_DANGEROUS_DESERIALIZATION in pdf_service: {ALLOW_DANGEROUS_DESERIALIZATION}")

def process_pdf(file_path: str) -> None:
    """处理上传的PDF文件"""
    try:
        # 加载PDF文件
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        logger.info(f"Loaded PDF: {file_path}")

        # 分割文本
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        logger.info(f"Split PDF into {len(texts)} chunks")

        # 初始化嵌入模型
        embeddings = OllamaEmbeddings(base_url=OLLAMA_BASE_URL, model="nomic-embed-text")

        # 创建或更新FAISS索引
        index_name = Path(file_path).stem
        index_path = f"{DB_PATH}/{index_name}.faiss"
        
        # 如果索引已存在，先删除旧索引
        if os.path.exists(index_path):
            os.remove(index_path)
            logger.info(f"Existing FAISS index removed: {index_path}")
        
        # 创建新的FAISS索引
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(DB_PATH, index_name)
        logger.info(f"Created new FAISS index: {index_path}")
        
        # 添加这行来确认文件是否存在
        logger.info(f"FAISS index file exists: {Path(index_path).exists()}")

    except Exception as e:
        logger.error(f"Error processing PDF {file_path}: {str(e)}")
        raise

def get_relevant_chunks(query: str, file_name: str, k: int = 4) -> List[str]:
    """从FAISS索引中检索与查询相关的文本块"""
    try:
        index_name = Path(file_name).stem.replace('.pdf', '')  # 移除 .pdf 扩展名
        embeddings = OllamaEmbeddings(base_url=OLLAMA_BASE_URL, model="nomic-embed-text")
        vectorstore = FAISS.load_local(DB_PATH, embeddings, index_name, allow_dangerous_deserialization=ALLOW_DANGEROUS_DESERIALIZATION)
        relevant_chunks = vectorstore.similarity_search(query, k=k)
        return [chunk.page_content for chunk in relevant_chunks]
    except Exception as e:
        logger.error(f"Error retrieving chunks for query '{query}': {str(e)}")
        raise

def get_file_list() -> List[str]:
    """获取上传的PDF文件列表"""
    try:
        files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.pdf')]
        return sorted(files)
    except Exception as e:
        logger.error(f"Error getting file list: {str(e)}")
        raise