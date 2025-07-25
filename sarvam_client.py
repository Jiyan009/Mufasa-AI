import requests
import json
from typing import List, Dict, Any, Optional
import streamlit as st


class SarvamClient:
    """Client for Sarvam AI + Weather API"""

    def __init__(self, api_key: str):
        """Initialize SarvamClient with Sarvam API key + Weather API key from secrets"""
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai/v1"
        self.headers = {
            "api-subscription-key": api_key,
            "Content-Type": "application/json"
        }
        # Use Streamlit secrets for weather too
        self.weather_api_key = st.secrets.get("WEATHER_API_KEY")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "sarvam-m",
        temperature: float = 0.8,
        top_p: float = 0.9,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        wiki_grounding: bool = False
    ) -> Dict[str, Any]:
        """Call Sarvam AI chat completion"""
        url = f"{self.base_url}/chat/completions"

        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "wiki_grounding": wiki_grounding
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if stop is not None:
            payload["stop"] = stop

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
                        "raw_response": data
                    }
                else:
                    return {"success": False, "error": "No response choices returned."}
            else:
                error_msg = response.json().get("error", {}).get("message", f"HTTP {response.status_code}")
                return {"success": False, "error": f"API error: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": f"Request error: {str(e)}"}

    def translate_text(
        self,
        text: str,
        source_language: str = "en-IN",
        target_language: str = "hi-IN",
        speaker_gender: str = "Male",
        mode: str = "formal"
    ) -> Dict[str, Any]:
        """Translate text"""
        url = f"{self.base_url}/translate"

        payload = {
            "input": text,
            "source_language_code": source_language,
            "target_language_code": target_language,
            "speaker_gender": speaker_gender,
            "mode": mode,
            "model": "mayura:v1",
            "enable_preprocessing": True
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "translated_text": data.get("translated_text", ""),
                    "raw_response": data
                }
            else:
                return {"success": False, "error": f"Translation failed: HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": f"Translation error: {str(e)}"}

    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language"""
        url = f"{self.base_url}/detect-language"
        payload = {"input": text}

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
