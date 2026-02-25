import os
from typing import List, Dict, Any, Generator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from llm.base import BaseLLMHandler
from dotenv import load_dotenv

load_dotenv()

class GeminiHandler(BaseLLMHandler):
    """
    Google Gemini LLM 处理器，使用 ChatGoogleGenerativeAI 实现。
    """

    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.7, **kwargs: Any):
        """
        初始化 Gemini 处理器。
        
        Args:
            model_name: Gemini 模型标识符
            temperature: 温度系数
            **kwargs: 其他传递给 ChatGoogleGenerativeAI 的参数
        """
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("未找到环境变量 GOOGLE_API_KEY")
            
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=self.api_key,
            **kwargs
        )

    @property
    def model(self) -> ChatGoogleGenerativeAI:
        return self.llm


    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[BaseMessage]:
        """将字典格式消息转换为 LangChain 消息对象"""
        lc_messages = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
        return lc_messages

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        lc_messages = self._convert_messages(messages)
        response = self.llm.invoke(lc_messages, **kwargs)
        return response.content

    def stream(self, messages: List[Dict[str, str]], **kwargs: Any) -> Generator[str, None, None]:
        lc_messages = self._convert_messages(messages)
        for chunk in self.llm.stream(lc_messages, **kwargs):
            yield chunk.content
