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
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% {
            transform: translate3d(0,0,0);
        }
        40%, 43% {
            transform: translate3d(0,-30px,0);
        }
        70% {
            transform: translate3d(0,-15px,0);
        }
        90% {
            transform: translate3d(0,-4px,0);
        }
    }
    
    @keyframes shake {
        0%, 100% {
            transform: translateX(0);
        }
        10%, 30%, 50%, 70%, 90% {
            transform: translateX(-10px);
        }
        20%, 40%, 60%, 80% {
            transform: translateX(10px);
        }
    }
    
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
        }
    }
    
    .bounce { animation-name: bounce; }
    .shake { animation-name: shake; animation-duration: 0.5s; }
    .spin { animation-name: spin; animation-duration: 1s; }
    .pulse { animation-name: pulse; animation-duration: 1.5s; animation-iteration-count: infinite; }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .error-message {
        background-color: #ff4b4b;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .loading-message {
        background-color: #ffd700;
        color: #333;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Additional dark theme text styling */
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
    
    .tiger-svg-container {
        transition: transform 0.3s ease;
    }
    
    .tiger-svg-container.bounce {
        animation: bounce 2s ease-in-out;
    }
    
    .tiger-svg-container.shake {
        animation: shake 0.5s ease-in-out;
    }
    
    .tiger-svg-container.spin {
        animation: spin 1s linear;
    }
    
    .tiger-svg-container.pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .tiger-display {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .tiger-ascii {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 8px;
        margin-right: 1rem;
    }
    
    .tiger-mascot-svg {
        transition: transform 0.3s ease;
    }
    
    .tiger-mascot-svg.bounce {
        animation: bounce 2s ease-in-out;
    }
    
    .tiger-mascot-svg.shake {
        animation: shake 0.5s ease-in-out;
    }
    
    .tiger-mascot-svg.spin {
        animation: spin 1s linear;
    }
    
    .tiger-mascot-svg.pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .simple-tiger {
        transition: transform 0.3s ease;
    }
    
    .simple-tiger.bounce {
        animation: bounce 2s ease-in-out;
    }
    
    .simple-tiger.shake {
        animation: shake 0.5s ease-in-out;
    }
    
    .simple-tiger.spin {
        animation: spin 1s linear;
    }
    
    .simple-tiger.pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
    </style>
    """
    return dark_theme_css


def render_tiger_mascot(tiger_mascot, state):
    """Render the tiger mascot with animations"""
    animation_class = tiger_mascot.get_animation_class(state)
    
    # Use simple character-based tiger that will definitely work
    tiger_html = get_simple_tiger_html(state=state, animation_class=animation_class)
    st.markdown(tiger_html, unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Get clients
    sarvam_client = get_sarvam_client()
    tiger_mascot = get_tiger_mascot()
    language_support = get_language_support()
    
    # Apply theme
    if st.session_state.dark_mode:
        st.markdown(apply_dark_theme(), unsafe_allow_html=True)
        theme_icon = "☀️"
    else:
        st.markdown(apply_light_theme(), unsafe_allow_html=True)
        theme_icon = "🌙"
    
    # Theme toggle button
    theme_button_html = f"""
    <button class="theme-toggle" onclick="document.getElementById('theme-toggle-btn').click();">
        {theme_icon}
    </button>
    """
    st.markdown(theme_button_html, unsafe_allow_html=True)
    
    # Hidden button for theme toggle
    if st.button("", key="theme-toggle-btn", help="Toggle theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    
    # Main container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Header
    st.title("🦁 Mufasa AI")
    st.markdown("**Your wise AI companion powered by Sarvam AI - Ask Mufasa anything!**")
    
    # Language selection in header
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
        
        # Update selected language
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
    
    # Tiger mascot display
    render_tiger_mascot(tiger_mascot, st.session_state.tiger_state)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input with language-specific placeholder
    chat_placeholder = language_support.get_chat_placeholder(st.session_state.selected_language)
    if prompt := st.chat_input(chat_placeholder):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Set tiger to thinking state
        st.session_state.tiger_state = "thinking"
        render_tiger_mascot(tiger_mascot, st.session_state.tiger_state)
        
        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            thinking_message = language_support.get_thinking_message(st.session_state.selected_language)
            message_placeholder.markdown(f'<div class="loading-message">{thinking_message}</div>', unsafe_allow_html=True)
            
            try:
                # Prepare messages with Mufasa identity and language preference
                system_message = language_support.create_system_message_for_language(st.session_state.selected_language)
                
                # Add system message to the beginning if not already present
                messages_with_identity = st.session_state.messages.copy()
                if not messages_with_identity or messages_with_identity[0].get("role") != "system":
                    messages_with_identity.insert(0, system_message)
                else:
                    # Update existing system message with current language preference
                    messages_with_identity[0] = system_message
                
                # Call Sarvam AI API
                response = sarvam_client.chat_completion(
                    messages=messages_with_identity,
                    temperature=0.8
                )
                
                if response["success"]:
                    ai_response = response["message"]
                    
                    # Translate response if auto-translate is enabled and language is not English
                    if (st.session_state.auto_translate and 
                        st.session_state.selected_language != "en-IN" and
                        st.session_state.selected_language in language_support.supported_languages):
                        
                        # Try to translate the response
                        translation_result = sarvam_client.translate_text(
                            text=ai_response,
                            source_language="en-IN",
                            target_language=st.session_state.selected_language
                        )
                        
                        if translation_result["success"]:
                            translated_response = translation_result["translated_text"]
                            ai_response = f"{translated_response}\n\n---\n*Original (English):* {ai_response}"
                        else:
                            # If translation fails, show original with note
                            lang_name = language_support.get_language_name(st.session_state.selected_language)
                            ai_response = f"{ai_response}\n\n*Note: Could not translate to {lang_name}*"
                    
                    # Set tiger to excited state
                    st.session_state.tiger_state = "excited"
                    
                    # Display AI response
                    message_placeholder.markdown(ai_response)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                    # Trigger tiger animation
                    time.sleep(0.5)
                    st.session_state.tiger_state = "happy"
                    
                else:
                    # Handle API error
                    error_msg = f"❌ Error: {response.get('error', 'Unknown error occurred')}"
                    message_placeholder.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                    
                    st.session_state.tiger_state = "sad"
                    
            except Exception as e:
                # Handle unexpected errors
                error_msg = f"❌ Unexpected error: {str(e)}"
                message_placeholder.markdown(f'<div class="error-message">{error_msg}</div>', unsafe_allow_html=True)
                
                st.session_state.tiger_state = "confused"
        
        # Rerun to update tiger animation
        st.rerun()
    
    # Sidebar with information
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🦁 Mufasa - Your AI Companion")
        st.markdown("Mufasa is your wise AI assistant created by **Jeet Borah** (Jeet Bhai), always ready to help with guidance and knowledge.")
    
        
        # Show welcome message in selected language
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
        st.markdown("- **Thinking**: Processing your request")
        st.markdown("- **Happy**: Successfully responded")
        st.markdown("- **Excited**: Getting ready to respond")
        st.markdown("- **Sad**: Error occurred")
        st.markdown("- **Confused**: Unexpected error")
        
        st.markdown("### 💡 Tips")
        st.markdown("- Use the theme toggle in the top right")
        st.markdown("- Switch languages anytime using the dropdown")
        st.markdown("- Enable auto-translate for multilingual responses")
        st.markdown("- Call Mufasa by name for personalized responses")
        st.markdown("- Tiger reacts to every response")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.tiger_state = "idle"
            st.rerun()
        
        # API status
        api_key = os.getenv("SARVAM_API_KEY", "default_api_key")
        if api_key == "default_api_key":
            st.warning("⚠️ Using default API key. Set SARVAM_API_KEY environment variable for full functionality.")
        else:
            st.success("✅ API key configured")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
