# GermanAI-backend

**GermanAI-backend** is a modern, AI-powered backend for German language learning.
It provides grammar checking, smart translation, verb conjugation, example sentences, and quiz generation via a clean REST API—**all powered by open source AI models** and robust microservices.

---

## Features

- **Grammar Checking:** Uses [LanguageTool](https://languagetool.org/) for comprehensive German grammar, spelling, and style suggestions.
- **Self-hosted Translation:** Fast, private translation between German, English, and other languages using [LibreTranslate](https://libretranslate.com/).
- **LLM-Powered Example Sentences:** On-demand, AI-generated sentences for any word, tailored for learners.
- **Smart Verb Conjugation:** Get all forms of any German verb for any person/tense, using a simple API and enums for clarity.
- **Multiple Choice Quiz Generation:** Get four English options (one correct, three distractors) for any German word—great for learning and flashcards!
- **API-First Design:** All endpoints have strict typing, enums, and auto-validated requests—works beautifully with Swagger UI and frontend codegen.
- **Secure Authentication (optional):** Supports Keycloak + JWT for secure user APIs.
- **Easy Deployment:** One command with Docker Compose spins up the whole stack (API, LLM, grammar, translation, auth).

---

## Quick Start

1. **Clone the repository**

    ```bash
    git clone git@github.com:hemrajchauhan/GermanAI-backend.git
    cd GermanAI-backend
    ```
2. **Create a .env file**

   Create a file named `.env` in the project root (next to `docker-compose.yml`).  
   Fill in your Keycloak and other variables as shown below (replace with your own values):

    ```bash
    # .env (example values, replace with your own for production!)
    KEYCLOAK_URL_INTERNAL=http://keycloak:8080
    KEYCLOAK_URL_PUBLIC=http://localhost:8082
    KEYCLOAK_REALM=GermanAI
    KEYCLOAK_CLIENT_ID=germanai-backend
    KEYCLOAK_CLIENT_SECRET=supersecretkeycloakclientsecret
    
    KEYCLOAK_ADMIN=admin
    KEYCLOAK_ADMIN_PASSWORD=adminpassword123
    
    # Ollama LLM endpoint (internal Docker address)
    OLLAMA_URL=http://ollama:11434/api/generate
    
    # LanguageTool API (internal Docker address)
    LANGUAGETOOL_API=http://languagetool:8010/v2/check
    
    # LibreTranslate API (internal Docker address)
    TRANSLATE_API=http://libretranslate:5000/translate
    
    # CORS
    ALLOWED_ORIGINS=http://localhost:8080
    ```

4. **Build and run with Docker Compose**

    ```bash
    docker compose up --build
    ```
    
5. **Pull the Llama 3 model for Ollama (first time only)**

    ```bash
    docker exec -it ollama ollama pull llama3
    ```
       
6. **Access the API documentation**

    Visit [http://localhost:8080/docs](http://localhost:8080/docs) in your browser to see interactive Swagger UI for all endpoints.

## API Endpoints
### POST `/check-grammar`
Checks the grammar of German sentences using LanguageTool.
- **Request Body:** JSON
  ```json
  { "text": "Ich habe ein Hund." }

- **Response:**
JSON object containing grammar issues and suggestions.

### GET `/example-sentence`
Generate an AI-powered German sentence using the provided word.
- **Request Body:** String
  ```str
  ?word=machen
  
- **Response:** JSON
  ```json
  {
      "word": "machen",
      "sentence": "Hier ist ein deutscher Beispielsatz mit dem Wort \"machen\":\n\n\"Sie macht jeden Morgen ihre Hausaufgaben, bevor sie zum Mittagessen geht.\"\n\nIn diesem Satz verwendet das Verb \"macht\" die Bedeutung \"tun, verrichten\" und beschreibt den Prozess, wie die Person ihre Hausaufgaben erledigt."
  }

### GET `/verb-form`
Generate an AI-powered German sentence using the provided word.
- **Request Body:** String
  ```str
  ?verb=laufen&form=perfekt&person=er%2Fsie%2Fes
  
- **Response:** JSON
  ```json
  {
      "verb": "laufen",
      "form": "perfekt",
      "person": "er/sie/es",
      "result": "Das Verb \"laufen\" im Perfekt wird wie folgt konjugiert:\n\n* Er: ist gelaufen\n* Sie: ist gelaufen\n* Es: ist gelaufen"
  }

### GET `/mcq-meaning`
Get a multiple-choice quiz (four options) for the meaning of a German word.
- **Request Body:** String
  ```str
  ?word=verloren
  
- **Response:** JSON
  ```json
  {
      "word": "verloren",
      "options": [
        "Won",
        "Lost",
        "Famous",
        "Found"
      ],
      "answer": 1
  }
  ```
  **Note:** `"answer"` is a zero-based index (first option is 0).

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
- **FastAPI** — Modern, high-performance Python web API framework.
- **Ollama** — Self-hosted open-source LLM (Large Language Model) server (e.g., Llama 3 and more) for AI-powered sentence generation and quizzes.
- **LanguageTool** — Self-hosted open-source grammar, spelling, and style checker.
- **LibreTranslate** — Self-hosted machine translation API for German, English, and more.
- **Keycloak** — Self-hosted identity and access management (IAM) platform for authentication and JWT-based API security (optional).
- **Docker Compose** — Multi-container orchestration; makes it easy to run and manage all services locally or in production.
- **Pydantic** — Python data validation and settings management, including powerful type-safe enums for request/response models.

## Extending
- **Tune LLM prompts:** See app/services/llm_service.py to change AI behavior or add more features.
- **Plug in your own models:** Swap in any Ollama-supported LLMs as desired.

## License
This project is licensed under the Apache License 2.0.
See [LICENSE](https://github.com/hemrajchauhan/GermanAI-backend/blob/main/LICENSE) for details.

## Contributing
Pull requests and issues are welcome!
Open an issue to get started.

## Author
Hemraj Chauhan

## Acknowledgements
- [LanguageTool](https://languagetool.org/)
- [LibreTranslate](https://libretranslate.com/)
- [Ollama](https://ollama.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Keycloak](https://www.keycloak.org/)
- The open-source community!

## Happy coding and viel Erfolg beim Deutschlernen! 🇩🇪

