import os
from typing import List, Dict, Optional, Any
import groq
import google.generativeai as genai
from cerebras.cloud.sdk import Cerebras
from src.utils.config import settings
from loguru import logger

class FreeLLMRouter:
    def __init__(self):
        self.groq_client = groq.Groq(api_key=settings.GROQ_API_KEY)
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.gemini_model = None
        if settings.CEREBRAS_API_KEY:
            self.cerebras_client = Cerebras(api_key=settings.CEREBRAS_API_KEY)
        else:
            self.cerebras_client = None

    def _call_groq(self, prompt: str, system_prompt: str, model: str = "llama-3.3-70b-versatile") -> Optional[str]:
        try:
            logger.info(f"Attempting Groq call with model: {model}")
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                model=model,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.warning(f"Groq failed: {e}")
            return None

    def _call_gemini(self, prompt: str, system_prompt: str) -> Optional[str]:
        if not self.gemini_model: return None
        try:
            logger.info("Attempting Gemini 1.5 Flash call")
            response = self.gemini_model.generate_content(f"{system_prompt}\n\nUser: {prompt}")
            return response.text
        except Exception as e:
            logger.warning(f"Gemini failed: {e}")
            return None

    def _call_cerebras(self, prompt: str, system_prompt: str, model: str = "llama3.1-70b") -> Optional[str]:
        if not self.cerebras_client: return None
        try:
            logger.info(f"Attempting Cerebras call with model: {model}")
            completion = self.cerebras_client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                model=model,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.warning(f"Cerebras failed: {e}")
            return None

    def complete(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        res = self._call_groq(prompt, system_prompt)
        if res: return res
        res = self._call_gemini(prompt, system_prompt)
        if res: return res
        res = self._call_cerebras(prompt, system_prompt)
        if res: return res
        raise Exception("All LLM providers failed.")

llm_router = FreeLLMRouter()
