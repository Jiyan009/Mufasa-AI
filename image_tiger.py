"""
Image-based Tiger Mascot
Creates a tiger mascot using Unicode characters and CSS styling
"""

def get_tiger_face_html(state="idle", animation_class=""):
    """Create a tiger face using Unicode and CSS"""
    
    # Different face expressions based on state
    if state == "thinking":
        eyes = "👀"
        mouth = "🤔"
        extra = "💭"
    elif state == "happy":
        eyes = "😊"
        mouth = "😸"
        extra = "✨"
    elif state == "excited":
        eyes = "🤩"
        mouth = "😁"
        extra = "🎉"
    elif state == "sad":
        eyes = "😢"
        mouth = "😿"
        extra = "💧"
    elif state == "confused":
        eyes = "😵"
        mouth = "😖"
        extra = "❓"
    elif state == "celebrating":
        eyes = "🥳"
        mouth = "😸"
        extra = "🏆"
    else:  # idle
        eyes = "👁️"
        mouth = "😺"
        extra = "💤"
    
    html = f'''
    <div class="tiger-container">
        <div class="custom-tiger-mascot {animation_class}">
            <div class="tiger-head">
                <div class="tiger-ears">🐯</div>
                <div class="tiger-face">
                    <div class="tiger-stripes">🟠⚫🟠⚫🟠</div>
                    <div class="tiger-eyes">{eyes}</div>
                    <div class="tiger-nose">👃</div>
                    <div class="tiger-mouth">{mouth}</div>
                    <div class="tiger-whiskers">╱ ╲   ╱ ╲</div>
                </div>
                <div class="tiger-extra">{extra}</div>
            </div>
        </div>
    </div>
    '''
    
    return html

def get_simple_tiger_html(state="idle", animation_class=""):
    """Get a very simple tiger representation that will work"""
    
    # Tiger states with different characters
    tiger_chars = {
        "idle": "🐯",
        "thinking": "🤔🐯", 
        "happy": "🐯🐯",
        "excited": "🤩🐯",
        "sad": "🐯X🐯",
        "confused": "😵🐯",
        "celebrating": "🥳🐯"
    }
    
    tiger_char = tiger_chars.get(state, "🐯")
    
    # Simple but effective HTML
    html = f'''
    <div class="tiger-container">
        <div class="simple-tiger {animation_class}">
            <div style="font-size: 6rem; text-align: center; line-height: 1.2;">
                {tiger_char}
            </div>
            <div style="font-size: 1rem; text-align: center; margin-top: 0.5rem; font-weight: bold; color: #333;">
                Tiger is {state}
            </div>
        </div>
    </div>
    '''
    
    return html
