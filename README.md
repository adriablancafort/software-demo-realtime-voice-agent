# Software Demo Real-Time Voice Agent

[<img src="https://img.youtube.com/vi/up1TkhqORCs/sddefault.jpg" alt="Demo Video" style="width: 100%;">](https://www.youtube.com/watch?v=up1TkhqORCs "Watch the demo video")

## 🚀 Features

- **Real-Time Interaction**: Instant responses and actions based on voice input
- **Customizable Experience**: Easily adapt to your SaaS application
- **Seamless Browser Automation**: Powered by Playwright for reliable web interactions

## 🏗️ How It Works

This Voice Agent Architecture is split into 3 different layers:

### 1. Speech-to-Text (STT) Layer 🎤
- **Provider**: Deepgram
- Converts user's spoken words into text in real-time
- Handles various accents and speech patterns with high accuracy
- **Voice Activity Detection**: Uses SileroVADAnalyzer for intelligent endpointing and turn detection

### 2. Large Language Model (LLM) Layer 🧠
- **Provider**: OpenAI (GPT-4)
- The brain of the operation where all the logic happens
- Processes user requests, understands context, and decides on actions
- Makes intelligent tool calls to navigate and interact with the application

### 3. Text-to-Speech (TTS) Layer 🔊
- **Provider**: Cartesia
- Converts AI responses back into natural-sounding speech
- Uses advanced voice synthesis for a professional, engaging experience

### Browser Automation 🌐
- **Technology**: Playwright
- Handles all web interactions, navigation, and UI manipulations
- Includes visual cursor animations for a polished demo experience

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- API keys from the following services:
  - [Deepgram](https://deepgram.com/) for speech-to-text
  - [OpenAI](https://openai.com/) for the language model
  - [Cartesia](https://cartesia.ai/) for text-to-speech

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/adriablancafort/software-demo-realtime-voice-agent.git
   cd software-demo-realtime-voice-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with your API keys:
   ```
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   CARTESIA_API_KEY=your_cartesia_api_key_here
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Access the demo**:
   - Open your browser and navigate to `http://localhost:7860/client/`
   - Click "Connect" to start the voice interaction
   - Enjoy your personalized software demo! 🎉

## 🎨 Customization for Your SaaS

To adapt this agent for your own SaaS application:

1. **Update Prompts**: Modify the prompts in `custom/prompts.py` to match your application's context and use cases
2. **Configure Selectors**: Update the CSS selectors in `custom/selectors.py` to target the specific elements in your web application

The agent uses tool calls to perform actions like:
- Navigating between pages
- Clicking on elements
- Typing into input fields
- Scrolling the page

Simply update the selectors and prompts to point to your application's UI elements and workflows.