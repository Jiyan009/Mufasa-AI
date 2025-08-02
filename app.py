import streamlit as st
import time
import requests
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
    """Dark theme styling"""
    return """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    /* Add your dark theme styles here */
    </style>
    """

def apply_light_theme():
    """Light theme styling"""
    return """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    /* Add your light theme styles here */
    </style>
    """

def render_tiger_mascot(tiger_mascot, state):
    animation_class = tiger_mascot.get_animation_class(state)
    tiger_html = get_simple_tiger_html(state=state, animation_class=animation_class)
    st.markdown(tiger_html, unsafe_allow_html=True)

# ✅ ✅ ✅ UPDATED: WeatherAPI version
def get_weather(city: str):
    api_key = st.secrets.get("WEATHER_API_KEY", "default_weather_api_key")
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            location = data["location"]["name"]
            region = data["location"]["region"]
            country = data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            feelslike_c = data["current"]["feelslike_c"]
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]

            result = (
                f"**Weather in {location}, {region}, {country}**\n"
                f"- Condition: {condition}\n"
                f"- Temperature: {temp_c}°C (Feels like {feelslike_c}°C)\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_kph} kph"
            )
            return result
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            return f"❌ Could not fetch weather: {error_message}"

    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"

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
        if prompt.lower().startswith("weather in"):
            city_name = prompt[10:].strip()
            weather = get_weather(city_name)
            st.session_state.messages.append({"role": "assistant", "content": weather})
            with st.chat_message("assistant"):
                st.markdown(weather)
            st.session_state.tiger_state = "happy"
            st.rerun()
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
        st.markdown("Mufasa is your wise AI assistant created by **Jeet Borah**. Powered by Sarvam AI, always ready to help.")
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

        st.markdown("### ☁️ Weather")
        city = st.text_input("Enter city name for weather")
        if st.button("🔍 Get Weather"):
            if city:
                weather_report = get_weather(city)
                st.info(weather_report)
            else:
                st.warning("Please enter a city name.")

        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.tiger_state = "idle"
            st.rerun()

        sarvam_api_key = st.secrets.get("SARVAM_API_KEY", "default_api_key")
        if sarvam_api_key == "default_api_key":
            st.warning("⚠️ Using default Sarvam API key. Set SARVAM_API_KEY for full functionality.")
        else:
            st.success("✅ SARVAM API key configured")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
