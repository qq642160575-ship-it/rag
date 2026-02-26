import os
import yaml
from typing import Dict, Any, Optional


class PromptManager:
    """
    统一管理 LLM 提示词。
    支持从 yaml 文件加载系统提示词和用户提示词模板。
    """

    def __init__(self, prompt_dir: str):
        self.prompt_dir = prompt_dir
        self.prompts: Dict[str, Dict[str, str]] = {}

    def _load_prompt(self, name: str) -> Dict[str, str]:
        if name not in self.prompts:
            file_path = os.path.join(self.prompt_dir, f"{name}.yaml")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Prompt file not found: {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                self.prompts[name] = content
        return self.prompts[name]

    def get_prompt(self, name: str, **kwargs) -> Dict[str, str]:
        """
        获取格式化后的提示词。
        返回包含 'system' 和 'user' 键的字典。
        """
        prompt_config = self._load_prompt(name)
        
        system_tmpl = prompt_config.get("system", "")
        user_tmpl = prompt_config.get("user", "")
        
        # 格式化变量
        system_prompt = system_tmpl.format(**kwargs) if system_tmpl else ""
        user_prompt = user_tmpl.format(**kwargs) if user_tmpl else ""
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }

    def get_langchain_messages(self, name: str, **kwargs) -> list:
        """
        获取 LangChain 格式的消息列表。
        """
        from langchain_core.messages import SystemMessage, HumanMessage
        
        prompts = self.get_prompt(name, **kwargs)
        messages = []
        if prompts["system"]:
            messages.append(SystemMessage(content=prompts["system"]))
        if prompts["user"]:
            messages.append(HumanMessage(content=prompts["user"]))
        return messages
