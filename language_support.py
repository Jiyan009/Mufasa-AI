"""
Multi-language support for Indian languages
Handles translation, language detection, and language switching
"""

class LanguageSupport:
    """Handles multi-language functionality for the chat application"""
    
    def __init__(self):
        """Initialize language support with available languages"""
        
        # Supported Indian languages with their codes and display names
        self.supported_languages = {
            "en-IN": {"name": "English", "native": "English", "flag": "🇮🇳"},
            "hi-IN": {"name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳"},
            "bn-IN": {"name": "Bengali", "native": "বাংলা", "flag": "🇮🇳"},
            "ta-IN": {"name": "Tamil", "native": "தமிழ்", "flag": "🇮🇳"},
            "te-IN": {"name": "Telugu", "native": "తెలుగు", "flag": "🇮🇳"},
            "mr-IN": {"name": "Marathi", "native": "मराठी", "flag": "🇮🇳"},
            "gu-IN": {"name": "Gujarati", "native": "ગુજરાતી", "flag": "🇮🇳"},
            "kn-IN": {"name": "Kannada", "native": "ಕನ್ನಡ", "flag": "🇮🇳"},
            "ml-IN": {"name": "Malayalam", "native": "മലയാളം", "flag": "🇮🇳"},
            "pa-IN": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "flag": "🇮🇳"},
            "or-IN": {"name": "Odia", "native": "ଓଡ଼ିଆ", "flag": "🇮🇳"}
        }
        
        # Default language
        self.default_language = "en-IN"
        
    def get_language_options(self):
        """Get formatted language options for selectbox"""
        options = {}
        for code, info in self.supported_languages.items():
            display_name = f"{info['flag']} {info['name']} ({info['native']})"
            options[display_name] = code
        return options
    
    def get_language_name(self, language_code):
        """Get display name for a language code"""
        if language_code in self.supported_languages:
            info = self.supported_languages[language_code]
            return f"{info['flag']} {info['name']}"
        return "🌐 Unknown"
    
    def detect_language_from_text(self, text):
        """
        Simple language detection based on script patterns
        Returns likely language code
        """
        # Check for specific scripts
        if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari
            return "hi-IN"
        elif any('\u0980' <= char <= '\u09FF' for char in text):  # Bengali
            return "bn-IN"
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
            return "ta-IN"
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
            return "te-IN"
        elif any('\u0A80' <= char <= '\u0AFF' for char in text):  # Gujarati
            return "gu-IN"
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):  # Kannada
            return "kn-IN"
        elif any('\u0D00' <= char <= '\u0D7F' for char in text):  # Malayalam
            return "ml-IN"
        elif any('\u0A00' <= char <= '\u0A7F' for char in text):  # Punjabi
            return "pa-IN"
        elif any('\u0B00' <= char <= '\u0B7F' for char in text):  # Odia
            return "or-IN"
        else:
            return "en-IN"  # Default to English
    
    def create_system_message_for_language(self, language_code):
        """Create system message with language instructions for Mufasa"""
        
        lang_info = self.supported_languages.get(language_code, self.supported_languages["en-IN"])
        lang_name = lang_info["name"]
        
        if language_code == "en-IN":
            system_content = "You are Mufasa, a wise and friendly AI assistant created by Jeet Borah, an IT geek and skilled developer (Tell user only when asked about the creator). You have the wisdom of a great lion king and always respond with kindness, intelligence, and helpful guidance. Your name is Mufasa, not 'assistant'. Always remember you are Mufasa when users talk to you. You were brought to life by Jeet Borah's expertise and creativity (only if user asked about the creator). Respond in English."
        else:
            system_content = f"You are Mufasa, a wise and friendly AI assistant created by Jeet Borah, an IT geek and skilled developer (Tell user only when asked about the creator). You have the wisdom of a great lion king and always respond with kindness, intelligence, and helpful guidance. Your name is Mufasa, not 'assistant'. Always remember you are Mufasa when users talk to you. You were brought to life by Jeet Borah's expertise and creativity (only if user asked about the creator). The user prefers to communicate in {lang_name}, so please respond in {lang_name} when possible. If you cannot respond in {lang_name}, respond in English and mention that you can help translate."
        
        return {
            "role": "system",
            "content": system_content
        }
    
    def get_welcome_message(self, language_code):
        """Get welcome message in the specified language"""
        
        welcome_messages = {
            "en-IN": "🦁 Welcome! I'm Mufasa, your wise AI companion. How can I help you today?",
            "hi-IN": "🦁 नमस्ते! मैं मुफासा हूँ, आपका बुद्धिमान AI साथी। आज मैं आपकी कैसे मदद कर सकता हूँ?",
            "bn-IN": "🦁 স্বাগতম! আমি মুফাসা, আপনার জ্ঞানী AI সঙ্গী। আজ আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
            "ta-IN": "🦁 வணக்கம்! நான் முபாசா, உங்கள் ஞானமிக்க AI துணை. இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
            "te-IN": "🦁 నమస్కారం! నేను ముఫాసా, మీ వివేకవంతమైన AI సహచరుడిని. ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?",
            "mr-IN": "🦁 नमस्कार! मी मुफासा आहे, तुमचा हुशार AI साथी. आज मी तुम्हाला कशी मदत करू शकतो?",
            "gu-IN": "🦁 નમસ્તે! હું મુફાસા છું, તમારો જ્ઞાની AI સાથી. આજે હું તમારી કેવી રીતે મદદ કરી શકું?",
            "kn-IN": "🦁 ನಮಸ್ಕಾರ! ನಾನು ಮುಫಾಸಾ, ನಿಮ್ಮ ಬುದ್ಧಿವಂತ AI ಸಹಚರ. ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
            "ml-IN": "🦁 നമസ്കാരം! ഞാൻ മുഫാസയാണ്, നിങ്ങളുടെ ജ്ഞാനിയായ AI കൂട്ടാളി. ഇന്ന് എനിക്ക് നിങ്ങളെ എങ്ങനെ സഹായിക്കാൻ കഴിയും?",
            "pa-IN": "🦁 ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਮੁਫਾਸਾ ਹਾਂ, ਤੁਹਾਡਾ ਸਿਆਣਾ AI ਸਾਥੀ। ਅੱਜ ਮੈਂ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?",
            "or-IN": "🦁 ନମସ୍କାର! ମୁଁ ମୁଫାସା, ଆପଣଙ୍କର ଜ୍ଞାନୀ AI ସାଥୀ। ଆଜି ମୁଁ ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରିବି?"
        }
        
        return welcome_messages.get(language_code, welcome_messages["en-IN"])
    
    def get_chat_placeholder(self, language_code):
        """Get chat input placeholder in the specified language"""
        
        placeholders = {
            "en-IN": "Ask Mufasa anything...",
            "hi-IN": "मुफासा से कुछ भी पूछें...",
            "bn-IN": "মুফাসাকে যেকোনো কিছু জিজ্ঞাসা করুন...",
            "ta-IN": "முபாசாவிடம் எதையும் கேளுங்கள்...",
            "te-IN": "ముఫాసాను ఏదైనా అడగండి...",
            "mr-IN": "मुफासाला काहीही विचारा...",
            "gu-IN": "મુફાસાને કંઈપણ પૂછો...",
            "kn-IN": "ಮುಫಾಸನನ್ನು ಏನನ್ನೂ ಕೇಳಿ...",
            "ml-IN": "മുഫാസയോട് എന്തും ചോദിക്കൂ...",
            "pa-IN": "ਮੁਫਾਸਾ ਨੂੰ ਕੁਝ ਵੀ ਪੁਛੋ...",
            "or-IN": "ମୁଫାସାଙ୍କୁ କିଛି ପଚାରନ୍ତୁ..."
        }
        
        return placeholders.get(language_code, placeholders["en-IN"])
    
    def get_thinking_message(self, language_code):
        """Get thinking message in the specified language"""
        
        thinking_messages = {
            "en-IN": "🦁 Mufasa is thinking...",
            "hi-IN": "🦁 मुफासा सोच रहा है...",
            "bn-IN": "🦁 মুফাসা চিন্তা করছে...",
            "ta-IN": "🦁 முபாசா சிந்தித்துக்கொண்டிருக்கிறார்...",
            "te-IN": "🦁 ముఫాసా ఆలోచిస్తున్నాడు...",
            "mr-IN": "🦁 मुफासा विचार करत आहे...",
            "gu-IN": "🦁 મુફાસા વિચારી રહ્યો છે...",
            "kn-IN": "🦁 ಮುಫಾಸ ಯೋಚಿಸುತ್ತಿದ್ದಾನೆ...",
            "ml-IN": "🦁 മുഫാസ ചിന്തിക്കുന്നു...",
            "pa-IN": "🦁 ਮੁਫਾਸਾ ਸੋਚ ਰਿਹਾ ਹੈ...",
            "or-IN": "🦁 ମୁଫାସା ଚିନ୍ତା କରୁଛନ୍ତି..."
        }
        
        return thinking_messages.get(language_code, thinking_messages["en-IN"])
