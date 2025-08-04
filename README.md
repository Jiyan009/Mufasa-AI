# Mufasa AI - Wise AI Companion

A multilingual AI chat application powered by Sarvam AI, featuring Mufasa AI - an intelligent conversational companion created by **Jeet Borah** with advanced language support and dynamic interactions powered by Sarvam AI.

## Features

🦁 **Mufasa AI Personality**
- Wise AI companion with lion king personality
- Intelligent, kind, and helpful responses
- Personalized guidance and advice

🌐 **Multi-Language Support**
- 11 Indian languages supported: English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and Odia
- Native script display with proper Unicode support
- Auto-translation feature using Sarvam AI
- Language-specific UI elements and messages

🐅 **Interactive Tiger Mascot**
- Animated tiger mascot with multiple emotional states
- Reacts to user interactions and AI responses
- Visual feedback for thinking, happy, excited, sad, and confused states

🎨 **Modern Interface**
- Clean, responsive Streamlit interface
- Dark/light theme toggle
- Professional design with smooth animations

## Installation

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install streamlit requests
```

3. **Set up Sarvam AI API Key**
   - Get your API key from [Sarvam AI](https://api.sarvam.ai)
   - Set it as an environment variable:
   ```bash
   export SARVAM_API_KEY="your_api_key_here"
   ```
   - Or create a `.env` file:
   ```
   SARVAM_API_KEY=your_api_key_here
   ```

## Running the Application

```bash
streamlit run app.py --server.port 5000
```

The application will be available at `http://localhost:5000`

## Project Structure

```
mufasa-ai/
├── app.py                 # Main Streamlit application
├── sarvam_client.py       # Sarvam AI API client
├── language_support.py    # Multi-language functionality
├── tiger_mascot.py        # Tiger mascot animations and states
├── image_tiger.py         # Tiger visual components
├── README.md             # This file
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Key Components

### Language Support
- **11 Indian Languages**: Full support for major Indian languages
- **Smart Translation**: Auto-translate responses using Sarvam AI
- **Native Scripts**: Proper display of Devanagari, Bengali, Tamil, Telugu, and other scripts
- **Language Detection**: Automatic detection of input language

### AI Integration
- **Sarvam AI API**: Powered by advanced language models
- **Mufasa Personality**: System prompts for wise, helpful responses
- **Context Awareness**: Maintains conversation history and context

### Interactive Elements
- **Dynamic Mascot**: Tiger mascot with 6 emotional states
- **Real-time Feedback**: Visual responses to user interactions
- **Smooth Animations**: CSS-based animations for better UX

## Configuration

### Streamlit Configuration (.streamlit/config.toml)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### Environment Variables
- `SARVAM_API_KEY`: Your Sarvam AI API key (required)

## Usage

1. **Select Language**: Choose from 11 supported Indian languages
2. **Enable Auto-translate**: Check the box to translate responses
3. **Chat with Mufasa**: Ask questions and get wise, helpful responses
4. **Watch the Tiger**: See mascot reactions to conversations
5. **Toggle Theme**: Switch between light and dark modes

## Supported Languages

| Language | Native Name | Language Code |
|----------|-------------|---------------|
| English | English | en-IN |
| Hindi | हिन्दी | hi-IN |
| Bengali | বাংলা | bn-IN |
| Tamil | தமிழ் | ta-IN |
| Telugu | తెలుగు | te-IN |
| Marathi | मराठी | mr-IN |
| Gujarati | ગુજરાતી | gu-IN |
| Kannada | ಕನ್ನಡ | kn-IN |
| Malayalam | മലയാളം | ml-IN |
| Punjabi | ਪੰਜਾਬੀ | pa-IN |
| Odia | ଓଡ଼ିଆ | or-IN |

## API Integration

This application uses the Sarvam AI API for:
- **Chat Completions**: Conversational AI responses
- **Text Translation**: Multi-language support
- **Language Detection**: Automatic language identification

## Deployment

### Local Deployment
```bash
streamlit run app.py --server.port 5000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install streamlit requests

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port", "5000"]
```

### Cloud Deployment
- **Streamlit Cloud**: Upload to GitHub and deploy via Streamlit Cloud
- **Heroku**: Add a `Procfile` with `web: streamlit run app.py --server.port $PORT`
- **AWS/GCP**: Use container services with the Docker configuration

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `SARVAM_API_KEY` is set correctly
   - Check API key validity at Sarvam AI dashboard

2. **Port Already in Use**
   - Change the port in `.streamlit/config.toml`
   - Or use: `streamlit run app.py --server.port 8501`

3. **Unicode Display Issues**
   - Ensure your terminal/browser supports Unicode
   - Check font support for Indian scripts

4. **Translation Not Working**
   - Verify internet connection
   - Check Sarvam AI API status
   - Enable auto-translate checkbox

## License

This project is open source. Please ensure you comply with Sarvam AI's terms of service when using their API.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues related to:
- **Application**: Create an issue in the repository
- **Sarvam AI API**: Contact Sarvam AI support
- **Streamlit**: Check Streamlit documentation

---

**Created by:** Jeet Borah- IT Geek & Developer  
**Built with:** ❤️ using Streamlit and Sarvam AI
