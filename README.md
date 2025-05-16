# Japan Honeymoon Travel Assistant

A Telegram bot application designed to provide comprehensive, personalized travel assistance for honeymooners visiting Japan. The assistant helps users plan their trip, navigate around Japan, understand cultural customs, translate phrases, check weather conditions, find points of interest, and handle emergency situations.

## Features

- **Natural Language Interaction**: Communicate with the bot in natural language via Telegram
- **Location Services**: Get directions, nearby recommendations, and transport guidance
- **Weather Information**: Current conditions, forecasts, and activity recommendations
- **Translation Assistance**: Translate phrases and access pre-translated common expressions
- **Japan Travel Knowledge**: Information about cities, attractions, transportation, customs, and cuisine
- **Emergency Assistance**: Emergency contacts and guidance for travelers

## Technology Stack

- **Backend**: FastAPI (Python)
- **Bot Framework**: python-telegram-bot
- **LLM Integration**: 
  - Local: Ollama
  - Cloud: OpenAI/Anthropic (configurable)
- **External APIs**:
  - Google Maps
  - OpenWeatherMap
  - Translation services

## Setup

### Prerequisites

- Python 3.10+ 
- [Ollama](https://ollama.ai/) for local LLM (optional)
- Telegram bot token (from BotFather)
- API keys for Google Maps, OpenWeatherMap, etc.

### Installation

1. Clone the repository
   ```
   git clone <repository-url>
   cd japan-honeymoon-travel-assistant
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the example
   ```
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

### Running the Application

1. Start the API server
   ```
   python -m app.main
   ```

2. In a separate terminal, run the Telegram bot (when implemented)
   ```
   python -m app.bot
   ```

## Development

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- isort for import sorting
- mypy for type checking

To format code:
```
black .
isort .
```

To check code quality:
```
flake8
mypy .
```

### Testing

Run tests with pytest:
```
pytest
```

For test coverage:
```
pytest --cov=app --cov-report=html
```

## License

[Add license information here] 