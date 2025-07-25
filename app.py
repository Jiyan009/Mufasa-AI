import streamlit as st
import os
import time
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

# Initialize Sarvam client
@st.cache_resource
def get_sarvam_client():
    api_key = os.getenv("SARVAM_API_KEY", "default_api_key")
    return SarvamClient(api_key)

# Initialize tiger mascot
@st.cache_resource
def get_tiger_mascot():
    return TigerMascot()

# Initialize language support
@st.cache_resource
def get_language_support():
    return LanguageSupport()

def initialize_session_state():
    """Initialize session state variables"""
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

def apply_dark_theme():
    """Apply dark theme styling"""
    dark_theme_css = """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatMessage {
        background-color: #262730;
        border: 1px solid #3a3f4b;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
        border: 1px solid #3a3f4b;
    }
    .stButton > button {
        background-color: #ff6b35;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #e55a2b;
        transform: translateY(-1px);
    }
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: #ff6b35;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        font-size: 1.5rem;
        transition: all 0.3s ease;
    }
    .theme-toggle:hover {
        background: #e55a2b;
        transform: scale(1.1);
    }
    /* Common tiger container and mascot animations remain unchanged */
    .tiger-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    .tiger-mascot {
        font-size: 4rem;
        animation-duration: 2s;
        animation-timing-function: ease-in-out;
        animation-fill-mode: both;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    /* Additional dark theme elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #ffffff !important;
    }
    .stSidebar .stMarkdown {
        color: #ffffff !important;
    }
    .stChatInput > div > div > textarea {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #3a3f4b !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    </style>
    """
    return dark_theme_css

def apply_light_theme():
    """Apply custom dark-shade light theme (#121212)"""
    light_theme_css = """
    <style>
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stChatMessage {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        color: #e0e0e0;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #333333;
    }
    .stButton > button {
        background-color: #ff6b35;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #e55a2b;
        transform: translateY(-1px);
    }
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: #ff6b35;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        font-size: 1.5rem;
        transition: all 0.3s ease;
    }
    .theme-toggle:hover {
        background: #e55a2b;
        transform: scale(1.1);
    }
    .tiger-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    .tiger-mascot {
        font-size: 4rem;
        animation-duration: 2s;
        animation-timing-function: ease-in-out;
        animation-fill-mode: both;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #e0e0e0 !important;
    }
    .stSidebar .stMarkdown {
        color: #e0e0e0 !important;
    }
    .stChatInput > div > div > textarea {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
        border: 1px solid #333333 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #e0e0e0 !important;
    }
    </style>
    """
    return light_theme_css

def render_tiger_mascot(tiger_mascot, state):
    animation_class = tiger_mascot.get_animation_class(state)
    tiger_html = get_simple_tiger_html(state=state, animation_class=animation_class)
    st.markdown(tiger_html, unsafe_allow_html=True)

def main():
    initialize_session_state()

    sarvam_client = get_sarvam_client()
    tiger_mascot = get_tiger_mascot()
    language_support = get_language_support()

    if st.session_state.dark_mode:
        st.markdown(apply_dark_theme(), unsafe_allow_html=True)
        theme_icon = "☀️"
    else:
        st.markdown(apply_light_theme(), unsafe_allow_html=True)
        theme_icon = "🌙"

    theme_button_html = f"""
    <button class="theme-toggle" onclick="document.getElementById('theme-toggle-btn').click();">
        {theme_icon}
    </button>
    """
    st.markdown(theme_button_html, unsafe_allow_html=True)

    if st.button("", key="theme-toggle-btn", help="Toggle theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.title("🦁 Mufasa AI")
    st.markdown("**Your wise AI companion powered by Sarvam AI - Ask Mufasa anything!**")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        language_options = language_support.get_language_options()
        current_lang_display = None
        for display, code in language_options.items():
            if code == st.session_state.selected_language:
                current_lang_display = display
                break
        selected_display = st.selectbox(
            "🌐 Language",
            options=list(language_options.keys()),
            index=list(language_options.keys()).index(current_lang_display) if current_lang_display else 0,
            key="language_selector"
        )
        new_language = language_options[selected_display]
        if new_language != st.session_state.selected_language:
            st.session_state.selected_language = new_language
            st.rerun()

    with col3:
        st.session_state.auto_translate = st.checkbox(
            "🔄 Auto-translate",
            value=st.session_state.auto_translate,
            help="Automatically translate responses to your selected language"
        )

    render_tiger_mascot(tiger_mascot, st.session_state.tiger_state)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat_placeholder = language_support.get_chat_placeholder(st.session_state.selected_language)
    if prompt := st.chat_input(chat_placeholder):
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
                    message_placeholder.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    time.sleep(0.5)
                    st.session_state.tiger_state = "happy"
                else:
                    error_msg = f"❌ Error: {response.get('error', 'Unknown error occurred')}"
                    message_placeholder.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                    st.session_state.tiger_state = "sad"
            except Exception as e:
                message_placeholder.markdown(f'<div class="error-message">❌ Unexpected error: {str(e)}</div>', unsafe_allow_html=True)
                st.session_state.tiger_state = "confused"
        st.rerun()

    with st.sidebar:
        st.markdown("### 🦁 Mufasa - Your AI Companion")
        st.markdown("Mufasa is your wise AI assistant created by **Jeet Borah**, always ready to help.")
        welcome_msg = language_support.get_welcome_message(st.session_state.selected_language)
        st.info(welcome_msg)
        st.markdown("### 🌐 Language Features")
        current_lang = language_support.get_language_name(st.session_state.selected_language)
        st.markdown(f"**Current Language:** {current_lang}")
        st.markdown("- **11 Indian Languages** supported")
        st.markdown("- **Auto-translation** available")
        st.markdown("- **Language detection** from your input")
        st.markdown("- **Native script** support")
        st.markdown("### 🐅 Tiger Mascot States")
        st.markdown("- **Idle**: Waiting for your message")
        st.markdown("- **Thinking**: Processing")
        st.markdown("- **Happy**: Responded")
        st.markdown("- **Excited**: Preparing")
        st.markdown("- **Sad**: Error")
        st.markdown("- **Confused**: Unexpected error")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.tiger_state = "idle"
            st.rerun()
        api_key = os.getenv("SARVAM_API_KEY", "default_api_key")
        if api_key == "default_api_key":
            st.warning("⚠️ Using default API key. Set SARVAM_API_KEY for full functionality.")
        else:
            st.success("✅ API key configured")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
