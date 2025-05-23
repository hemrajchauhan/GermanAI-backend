# GermanAI-backend

**GermanAI-backend** is an open-source, AI-powered backend for German language learning apps.  
It provides grammar checking, word translation, and example sentences via a clean REST API.  
Built with FastAPI and Docker Compose, it’s easy to run locally or in the cloud.

---

## Features

- **Grammar Checking:** Uses LanguageTool for advanced German grammar, spelling, and style suggestions.
- **Word Translation & Examples:** Look up German words, their English meanings, and sample sentences from a customizable dictionary.
- **API-First Design:** Built for easy integration with cross-platform frontends (like .NET MAUI, web, or mobile).
- **Easy Deployment:** One command to spin up everything using Docker Compose.
- **Extensible:** Add support for more parts of speech, AI features, or languages as your project grows.

---

## Live Demo
The API is deployed and available at:

- [https://germanai-backend.fly.dev/](https://germanai-backend.fly.dev/)
- [Interactive Swagger UI Docs](https://germanai-backend.fly.dev/docs)

> Note: The root URL (`/`) returns `{"message":"Welcome to GermanAI-backend! Visit /docs for API documentation."}` by design. Use `/docs` or the listed endpoints for API access.

---

## Quick Start

1. **Clone the repository**

    ```bash
    git clone git@github.com:hemrajchauhan/GermanAI-backend.git
    cd GermanAI-backend
    ```

2. **Build and run with Docker Compose**

    ```bash
    docker compose up --build
    ```

3. **Access the API documentation**

    Visit [http://localhost:8080/docs](http://localhost:8080/docs) in your browser  
    (You’ll see interactive Swagger UI for all endpoints.)

## API Endpoints
### POST `/check-grammar`
Checks the grammar of German sentences using LanguageTool.
- **Request Body:** JSON
  ```json
  { "text": "Ich habe ein Hund." }

- **Response:**
JSON object containing grammar issues and suggestions.

### POST `/translate-word`
Translates a German word and returns example usage from the dictionary.

- **Request Body:** JSON
  ```json
  { "word": "laufen" }

- **Response:** JSON
  ```json
  {
  "type": "verb",
  "translation": "to run",
  "examples": ["Ich laufe jeden Morgen."]
  }

## Technology Stack
- **FastAPI** — Python async API framework
- **LanguageTool** — Open source grammar and spell checker (self-hosted via Docker)
- **Docker Compose** — Multi-container orchestration
- **Pydantic** — Data validation and parsing

## Extending
- **Dictionary**: Add more words and examples in app/static/dictionary.json.
- **Grammar explanations**: Extend the backend with AI or LLM-powered endpoints.
- **Other languages**: Adapt endpoints for additional languages or grammar tools.

## License
This project is licensed under the Apache License 2.0.
See [LICENSE](https://github.com/hemrajchauhan/GermanAI-backend/blob/main/LICENSE) for details.

## Contributing
Pull requests and issues are welcome!
Open an issue to get started.

## Author
Hemraj Chauhan

## Acknowledgements
- LanguageTool community for their excellent open-source grammar checker.
- FastAPI and Docker communities for making robust backend development approachable.

## Happy coding and viel Erfolg beim Deutschlernen! 🇩🇪

