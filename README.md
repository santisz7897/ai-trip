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
- **Deployment**: Docker

## Setup

### Prerequisites

- Python 3.10+ 
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- [Ollama](https://ollama.ai/) for local LLM (optional)
- Telegram bot token (from BotFather)
- API keys for Google Maps, OpenWeatherMap, etc.
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

1. Clone the repository
   ```
   git clone <repository-url>
   cd japan-honeymoon-travel-assistant
   ```

2. Create and activate a virtual environment using uv
   ```
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies using uv
   ```
   # Install from lock file (recommended for reproducible builds)
   uv pip install -r requirements.lock
   
   # Or install dependencies with development tools
   uv pip install -e ".[dev]"
   ```

4. Create a `.env` file based on the example
   ```
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

### Managing Dependencies

This project uses uv for dependency management:

- Add a new dependency:
  ```
  uv pip install package_name
  ```

- Update the lock file after changing pyproject.toml:
  ```
  uv pip compile pyproject.toml -o requirements.lock
  ```

- Install all dependencies from lock file:
  ```
  uv pip install -r requirements.lock
  ```

### Running the Application

#### Local Development

1. Start the API server
   ```
   python -m app.main
   ```

2. In a separate terminal, run the Telegram bot (when implemented)
   ```
   python -m app.bot
   ```

#### Using Docker

1. Build and start containers
   ```
   docker-compose up -d
   ```

   This will start the API server on port 8000. You can access it at http://localhost:8000.

2. View logs
   ```
   docker-compose logs -f
   ```

3. Stop containers
   ```
   docker-compose down
   ```

4. Rebuild containers after changes
   ```
   docker-compose up -d --build
   ```

5. Using Ollama with Docker (optional)
   - Uncomment the Ollama service in docker-compose.yml
   - Make sure your .env file has USE_LOCAL_LLM=True and OLLAMA_BASE_URL=http://ollama:11434
   ```
   docker-compose up -d
   ```
   - Pull your preferred model:
   ```
   docker-compose exec ollama ollama pull llama3
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