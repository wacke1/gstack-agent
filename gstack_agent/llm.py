"""LLM 客户端 - 支持 OpenAI / 自定义 API"""
import json
import os
import requests
from typing import Optional, List, Dict, Any, Union


def load_config() -> Dict[str, Any]:
    config_path = os.path.expanduser("~/.gstack-agent/config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}


class LLMClient:
    def __init__(self):
        self.config = load_config()
        self.api_key = (
            self.config.get("api_key", "")
            or os.environ.get("OPENAI_API_KEY", "")
            or os.environ.get("LLM_API_KEY", "")
        )
        self.base_url = (
            self.config.get("base_url", "")
            or os.environ.get("OPENAI_API_BASE", "")
            or os.environ.get("LLM_BASE_URL", "")
        )
        self.model = (
            self.config.get("model", "")
            or os.environ.get("OPENAI_MODEL", "")
            or os.environ.get("LLM_MODEL", "")
            or "gpt-4o"
        )

    def chat(
        self,
        messages: Union[str, List[Dict[str, str]]],
        max_tokens: int = 2000,
    ) -> str:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        if not self.api_key and not self.base_url:
            return self._mock_response(messages, max_tokens)

        url = self.base_url.rstrip("/") + "/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError) as e:
            return f"[LLM 调用失败：{e}]\n\n请检查 ~/.gstack-agent/config.json 或环境变量 LLM_API_KEY/LLM_BASE_URL/LLM_MODEL。"

    def _mock_response(self, messages: List[Dict[str, str]], max_tokens: int) -> str:
        last_content = ""
        for m in reversed(messages):
            if m["role"] == "user":
                last_content = m["content"]
                break
        if not last_content:
            last_content = messages[0]["content"]

        return (
            "\n[本地模式 - 未配置 LLM]\n\n"
            f"输入：{last_content[:200]}...\n\n"
            "请在 ~/.gstack-agent/config.json 中配置 LLM API 以启用完整功能：\n"
            "  {\"api_key\": \"sk-xxx\", \"base_url\": \"https://api.openai.com/v1\", \"model\": \"gpt-4o\"}\n"
            "或通过环境变量：export LLM_API_KEY=sk-xxx LLM_BASE_URL=... LLM_MODEL=gpt-4o"
        )


_llm_client = None

def get_llm_client() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client