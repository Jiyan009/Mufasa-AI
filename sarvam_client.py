import requests
import json
import os
from typing import List, Dict, Any, Optional

class SarvamClient:
    """Client for interacting with Sarvam AI API"""
    
    def __init__(self, api_key: str):
        """Initialize the Sarvam client with API key"""
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai/v1"
        self.headers = {
            "api-subscription-key": api_key,
            "Content-Type": "application/json"
        }
    
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
        """
        Get chat completion from Sarvam AI
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (default: sarvam-m)
            temperature: Controls randomness (0-2)
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate
            stop: List of stop sequences
            frequency_penalty: Penalize repetition (-2.0 to 2.0)
            presence_penalty: Encourage new topics (-2.0 to 2.0)
            wiki_grounding: Enable RAG with Wikipedia
        
        Returns:
            Dictionary with success status and response/error message
        """
        
        url = f"{self.base_url}/chat/completions"
        
        # Prepare the payload
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "wiki_grounding": wiki_grounding
        }
        
        # Add optional parameters
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        
        if stop is not None:
            payload["stop"] = stop
        
        try:
            # Make the API request
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                
                # Extract the message from the response
                if "choices" in data and len(data["choices"]) > 0:
                    message = data["choices"][0]["message"]["content"]
                    return {
                        "success": True,
                        "message": message,
                        "raw_response": data
                    }
                else:
                    return {
                        "success": False,
                        "error": "No response choices found in API response"
                    }
            
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid API key. Please check your SARVAM_API_KEY environment variable."
                }
            
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit exceeded. Please try again later."
                }
            
            elif response.status_code == 500:
                return {
                    "success": False,
                    "error": "Server error. Please try again later."
                }
            
            else:
                # Try to get error message from response
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                except:
                    error_message = f"HTTP {response.status_code}"
                
                return {
                    "success": False,
                    "error": f"API request failed: {error_message}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Please check your internet connection and try again."
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error. Please check your internet connection."
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid JSON response from API"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def translate_text(
        self,
        text: str,
        source_language: str = "en-IN",
        target_language: str = "hi-IN",
        speaker_gender: str = "Male",
        mode: str = "formal"
    ) -> Dict[str, Any]:
        """
        Translate text using Sarvam AI translation API
        
        Args:
            text: Text to translate
            source_language: Source language code (BCP-47 format)
            target_language: Target language code (BCP-47 format)
            speaker_gender: Male or Female
            mode: formal or informal
        
        Returns:
            Dictionary with success status and translated text or error
        """
        
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
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                translated_text = data.get("translated_text", "")
                return {
                    "success": True,
                    "translated_text": translated_text,
                    "raw_response": data
                }
            else:
                return {
                    "success": False,
                    "error": f"Translation failed: HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Translation error: {str(e)}"
            }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with success status and detected language or error
        """
        
        url = f"{self.base_url}/detect-language"
        
        payload = {
            "input": text
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "detected_language": data.get("detected_language"),
                    "confidence": data.get("confidence"),
                    "raw_response": data
                }
            else:
                return {
                    "success": False,
                    "error": f"Language detection failed: HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Language detection error: {str(e)}"
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Sarvam AI API
        
        Returns:
            Dictionary with success status and connection info
        """
        
        # Test with a simple chat completion
        test_messages = [{"role": "user", "content": "Hello"}]
        
        result = self.chat_completion(
            messages=test_messages,
            temperature=0.1
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "API connection successful"
            }
        else:
            return {
                "success": False,
                "error": f"API connection failed: {result.get('error', 'Unknown error')}"
            }
