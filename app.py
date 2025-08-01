import streamlit as st
import time
import requests
from serpapi import GoogleSearch  # 🆕 SERPAPI
from sarvam_client import SarvamClient
from tiger_mascot import TigerMascot
from image_tiger import get_simple_tiger_html
from language_support import LanguageSupport

# Page configuration
st.set_page_config(
    page_title="Mufasa AI - Your Wise AI Companion",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Sarvam client using st.secrets
@st.cache_resource
def get_sarvam_client():
    api_key = st.secrets.get("SARVAM_API_KEY", "default_api_key")
    return SarvamClient(api_key)

@st.cache_resource
def get_tiger_mascot():
    return TigerMascot()

@st.cache_resource
def get_language_support():
    return LanguageSupport()

# ✅ Full-featured SERPAPI Integration Function
def search_with_serpapi(query):
    api_key = st.secrets.get("SERPAPI_API_KEY", "")
    if not api_key:
        return "❌ SerpAPI key not found in secrets. Please set `SERPAPI_API_KEY` in Streamlit settings."

    params = {
        "engine": "google",
        "q": query,
        "location": "Seattle-Tacoma, WA, Washington, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "num": "10",
        "start": "0",
        "safe": "active",
        "api_key": api_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        if organic_results:
            output = "🔍 **Top Search Results:**\n\n"
            for res in organic_results[:5]:
                title = res.get("title", "")
                link = res.get("link", "")
                snippet = res.get("snippet", "")
                output += f"- **[{title}]({link})**\n  \n  _{snippet}_\n\n"
            return output
        else:
            return "❌ No search results found."
    except Exception as e:
        return f"❌ Error during search: {str(e)}"

# Session state initialization
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "tiger_state" not in st.session_state:
        st.session_state.tiger_state = "idle"
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en-IN"
    if "auto_translate" not in st.session_state:
        st.session_state.auto_translate = False

# Main function
def main():
    initialize_session_state()

    sarvam_client = get_sarvam_client()
    tiger_mascot = get_tiger_mascot()
    language_support = get_language_support()

    chat_placeholder = "Talk to Mufasa AI 🦁"

    if prompt := st.chat_input(chat_placeholder):
        response_content = ""

        if prompt.lower().startswith("weather in"):
            city_name = prompt[10:].strip()
            response_content = get_weather(city_name)

        elif prompt.lower().startswith("search for"):
            query = prompt[10:].strip()
            response_content = search_with_serpapi(query)  # 🆕 Full SerpAPI integration

        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.tiger_state = "thinking"
            render_tiger_mascot(tiger_mascot, st.session_state.tiger_state)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                thinking_message = language_support.get_thinking_message(st.session_state.selected_language)
                message_placeholder.markdown(f'<div class="loading-message">{thinking_message}</div>', unsafe_allow_html=True)
                try:
                    system_message = language_support.create_system_message_for_language(st.session_state.selected_language)
                    messages_with_identity = st.session_state.messages.copy()

                    if not messages_with_identity or messages_with_identity[0].get("role") != "system":
                        messages_with_identity.insert(0, system_message)
                    else:
                        messages_with_identity[0] = system_message

                    response = sarvam_client.chat_completion(messages=messages_with_identity, temperature=0.8)

                    if response["success"]:
                        ai_response = response["message"]
                        if (st.session_state.auto_translate and st.session_state.selected_language != "en-IN"):
                            translation_result = sarvam_client.translate_text(
                                text=ai_response,
                                source_language="en-IN",
                                target_language=st.session_state.selected_language
                            )
                            if translation_result["success"]:
                                translated = translation_result["translated_text"]
                                ai_response = f"{translated}\n\n---\n*Original (English):* {ai_response}"

                        st.session_state.tiger_state = "excited"
                        response_content = ai_response
                        message_placeholder.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        time.sleep(0.5)
                        st.session_state.tiger_state = "happy"

                    else:
                        error_msg = f"❌ Error: {response.get('error', 'Unknown error occurred')}"
                        response_content = error_msg
                        message_placeholder.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                        st.session_state.tiger_state = "sad"

                except Exception as e:
                    response_content = f"❌ Unexpected error: {str(e)}"
                    message_placeholder.markdown(f'<div class="error-message">{response_content}</div>', unsafe_allow_html=True)
                    st.session_state.tiger_state = "confused"

        if response_content:
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            with st.chat_message("assistant"):
                st.markdown(response_content)
            st.rerun()

# 🔁 Run app
if __name__ == "__main__":
    main()
