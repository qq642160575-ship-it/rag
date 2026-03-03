from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator, Union

from langchain_core.callbacks import BaseCallbackHandler


class BaseLLMHandler(ABC):
    """
    LLM 处理器基类，定义统一的接口契约。
    """

    @property
    @abstractmethod
    def model(self) -> Any:
        """
        获取底层 LangChain 模型对象。
        用于直接调用模型的高级功能，如 .with_structured_output() 或在 LangGraph 节点中使用。
        """
        pass

    def invoke(self, input: Any, **kwargs: Any) -> Any:
        """
        兼容 LangChain 的 invoke 方法，直接透传给底层模型。
        """
        return self.model.invoke(input, **kwargs)

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """
        同步调用大模型（封装后的统一接口）。
        """
        pass

    @abstractmethod
    def stream(self, messages: List[Dict[str, str]], **kwargs: Any) -> Generator[str, None, None]:
        """
        流式调用大模型（封装后的统一接口）。
        """
        pass


class DebugHandler(BaseCallbackHandler):

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("\n========== 发送给模型的 Prompt ==========")
        for p in prompts:
            print(p)

    def on_llm_end(self, response, **kwargs):
        print("\n========== 模型原始返回 ==========")
        print(response)