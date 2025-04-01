import logging
from typing import List, Tuple
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from config import OLLAMA_BASE_URL, DB_PATH, ALLOW_DANGEROUS_DESERIALIZATION
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def get_ollama_model(model_name: str):
    return Ollama(base_url=OLLAMA_BASE_URL, model=model_name)

def get_ollama_embeddings(model_name: str):
    return OllamaEmbeddings(base_url=OLLAMA_BASE_URL, model=model_name)

def get_chat_response(query: str, file_name: str, chat_history: List[Tuple[str, str]]) -> str:
    try:
        # 初始化 Ollama 模型
        llm = get_ollama_model("qwen2")
        
        # 初始化嵌入模型
        embeddings = get_ollama_embeddings("nomic-embed-text")
        
        # 加载 FAISS 索引
        index_name = Path(file_name).stem.replace('.pdf', '')  # 移除 .pdf 扩展名
        index_path = f"{DB_PATH}/{index_name}.faiss"
        logger.info(f"Attempting to load FAISS index from: {index_path}")
        logger.info(f"FAISS index file exists: {os.path.exists(index_path)}")
        
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index file not found: {index_path}")
        
        vectorstore = FAISS.load_local(DB_PATH, embeddings, index_name, allow_dangerous_deserialization=ALLOW_DANGEROUS_DESERIALIZATION)
        
        # 创建对话记忆
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 自定义提示模板
        prompt_template = """请仔细阅读以下上下文信息，并基于此回答问题。如果上下文中没有相关信息或你不确定答案，请诚实地表示不知道。请不要编造或猜测任何信息。回答时，请使用简洁明了的语言，并尽可能提供具体和相关的细节。如果问题涉及多个方面，请有条理地逐点回答。
        
上下文: {context}

人类: {question}

AI助手: """
        
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        # 创建对话检索链
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": PROMPT}
        )
        
        # 处理聊天历史
        for human, ai in chat_history:
            memory.chat_memory.add_user_message(human)
            memory.chat_memory.add_ai_message(ai)
        
        # 生成响应
        response = qa_chain({"question": query})
        
        # 打印发送给 Ollama 的 prompt
        logger.info(f"Prompt sent to Ollama: {response['question']}")
        logger.info(f"Context sent to Ollama: {response['chat_history']}")
        
        logger.info(f"Generated response for query: {query}")
        return response['answer']
    
    except FileNotFoundError as e:
        logger.error(f"FAISS index file not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error generating chat response: {str(e)}")
        raise

def get_model_info():
    try:
        llm = get_ollama_model("qwen2")
        embeddings = get_ollama_embeddings("nomic-embed-text")
        
        llm_info = llm.model_info()
        embeddings_info = embeddings.model_info()
        
        return {
            "llm": llm_info,
            "embeddings": embeddings_info
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return {"error": str(e)}